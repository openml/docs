"""
Callbacks module contains classes and functions for handling callback functions during an event-driven process. This makes it easier to customize the behavior of the training loop and add additional functionality to the training process without modifying the core code.

To use a callback, create a class that inherits from the Callback class and implement the necessary methods. Callbacks can be used to perform actions at different stages of the training process, such as at the beginning or end of an epoch, batch, or fitting process. Then pass the callback object to the Trainer.
"""

from functools import partial
import math
import re
from typing import Iterable

from matplotlib import pyplot as plt
import numpy as np
import torch

_camel_re1 = re.compile("(.)([A-Z][a-z]+)")
_camel_re2 = re.compile("([a-z0-9])([A-Z])")
torch.Tensor.ndim = property(lambda x: len(x.shape))


def listify(o = None) -> list:
    """
    Convert `o` to list. If `o` is None, return empty list.
    """
    if o is None:
        return []
    if isinstance(o, list):
        return o
    if isinstance(o, str):
        return [o]
    if isinstance(o, Iterable):
        return list(o)
    return [o]


def annealer(f) -> callable:
    """
    A decorator function for creating a partially applied function with predefined start and end arguments.
    The inner function `_inner` captures the `start` and `end` parameters and returns a `partial` object that fixes these parameters for the decorated function `f`.
    """
    def _inner(start, end):
        return partial(f, start, end)

    return _inner


@annealer
def sched_lin(start: float, end: float, pos: float) -> float:
    """
    A linear schedule function.
    """
    return start + pos * (end - start)


@annealer
def sched_cos(start: float, end: float, pos: float) -> float:
    """
    A cosine schedule function.
    """
    return start + (1 + math.cos(math.pi * (1 - pos))) * (end - start) / 2


@annealer
def sched_no(start: float, end: float, pos: float) -> float:
    """
    Disabled scheduling.
    """
    return start


@annealer
def sched_exp(start: float, end: float, pos: float) -> float:
    """
    Exponential schedule function.
    """
    return start * (end / start) ** pos


def combine_scheds(pcts: Iterable[float], scheds: Iterable[callable]) -> callable:
    """
    Combine multiple scheduling functions.
    """
    assert sum(pcts) == 1.0
    pcts = torch.tensor([0] + listify(pcts))
    assert torch.all(pcts >= 0)
    pcts = torch.cumsum(pcts, 0)

    def _inner(pos):
        idx = (pos >= pcts).nonzero().max()
        actual_pos = (pos - pcts[idx]) / (pcts[idx + 1] - pcts[idx])
        return scheds[idx](actual_pos)

    return _inner


def camel2snake(name : str) -> str:
    """
    Convert `name` from camel case to snake case.
    """
    s1 = re.sub(_camel_re1, r"\1_\2", name)
    return re.sub(_camel_re2, r"\1_\2", s1).lower()


class Callback:
    """

        Callback class is a base class designed for handling different callback functions during
        an event-driven process. It provides functionality to set a runner, retrieve the class
        name in snake_case format, directly call callback methods, and delegate attribute access
        to the runner if the attribute does not exist in the Callback class.

        The _order is used to decide the order of Callbacks.

    """
    _order = 0

    def set_runner(self, run) -> None:
        self.run = run

    @property
    def name(self):
        name = re.sub(r"Callback$", "", self.__class__.__name__)
        return camel2snake(name or "callback")

    def __call__(self, cb_name):
        f = getattr(self, cb_name, None)
        if f and f():
            return True
        return False

    def __getattr__(self, k):
        return getattr(self.run, k)


class ParamScheduler(Callback):
    """
    Manages scheduling of parameter adjustments over the course of training.
    """
    _order = 1

    def __init__(self, pname, sched_funcs):
        self.pname, self.sched_funcs = pname, sched_funcs

    def begin_fit(self):
        """
        Prepare the scheduler at the start of the fitting process.
        This method ensures that sched_funcs is a list with one function per parameter group.
        """
        if not isinstance(self.sched_funcs, (list, tuple)):
            self.sched_funcs = [self.sched_funcs] * len(self.opt.param_groups)

    def set_param(self):
        """
        Adjust the parameter value for each parameter group based on the scheduling function.
        Ensures the number of scheduling functions matches the number of parameter groups.
        """
        assert len(self.opt.param_groups) == len(self.sched_funcs)
        for pg, f in zip(self.opt.param_groups, self.sched_funcs):
            pg[self.pname] = f(self.n_epochs / self.epochs)

    def begin_batch(self):
        """
        Apply parameter adjustments at the beginning of each batch if in training mode.
        """
        if self.in_train:
            self.set_param()

class Recorder(Callback):
    """
        Recorder is a callback class used to record learning rates and losses during the training process.
    """
    def begin_fit(self):
        """
        Initializes attributes necessary for the fitting process.

        Sets up learning rates and losses storage.

        Attributes:
            self.lrs (list): A list of lists, where each inner list will hold learning rates for a parameter group.
            self.losses (list): An empty list to store loss values during the fitting process.
        """
        self.lrs = [[] for _ in self.opt.param_groups]
        self.losses = []

    def after_batch(self):
        """
        Handles operations to execute after each training batch.

        Modifies the learning rate for each parameter group in the optimizer 
        and appends the current learning rate and loss to the corresponding lists.

        """
        if not self.in_train:
            return
        for pg, lr in zip(self.opt.param_groups, self.lrs):
            lr.append(pg["lr"])
        self.losses.append(self.loss.detach().cpu())

    def plot_lr(self, pgid=-1):
        """
        Plots the learning rate for a given parameter group.
        """
        plt.plot(self.lrs[pgid])

    def plot_loss(self, skip_last=0):
        """
        Plots the loss for a given parameter group.
        """
        plt.plot(self.losses[: len(self.losses) - skip_last])

    def plot(self, skip_last=0, pgid=-1):
        """
        Generates a plot of the loss values against the learning rates.
        """
        losses = [o.item() for o in self.losses]
        lrs = self.lrs[pgid]
        n = len(losses) - skip_last
        plt.xscale("log")
        plt.plot(lrs[:n], losses[:n])


class TrainEvalCallback(Callback):
    """
        TrainEvalCallback class is a custom callback used during the training
        and validation phases of a machine learning model to perform specific
        actions at the beginning and after certain events.

        Methods:

        begin_fit():
            Initialize the number of epochs and iteration counts at the start
            of the fitting process.

        after_batch():
            Update the epoch and iteration counts after each batch during
            training.

        begin_epoch():
            Set the current epoch, switch the model to training mode, and
            indicate that the model is in training.

        begin_validate():
            Switch the model to evaluation mode and indicate that the model
            is in validation.
    """
    def begin_fit(self):
        self.run.n_epochs = 0
        self.run.n_iter = 0

    def after_batch(self):
        if not self.in_train:
            return
        self.run.n_epochs += 1.0 / self.iters
        self.run.n_iter += 1

    def begin_epoch(self):
        self.run.n_epochs = self.epoch
        self.model.train()
        self.run.in_train = True

    def begin_validate(self):
        self.model.eval()
        self.run.in_train = False


class CancelTrainException(Exception):
    pass


class CancelEpochException(Exception):
    pass


class CancelBatchException(Exception):
    pass


class AvgStats:
    """
    AvgStats class is used to track and accumulate average statistics (like loss and other metrics) during training and validation phases.

    Attributes:
        metrics (list): A list of metric functions to be tracked.
        in_train (bool): A flag to indicate if the statistics are for the training phase.

    Methods:
        __init__(metrics, in_train):
            Initializes the AvgStats with metrics and in_train flag.

        reset():
            Resets the accumulated statistics.

        all_stats:
            Property that returns all accumulated statistics including loss and metrics.

        avg_stats:
            Property that returns the average of the accumulated statistics.

        accumulate(run):
            Accumulates the statistics using the data from the given run.

        __repr__():
            Returns a string representation of the average statistics.
    """
    def __init__(self, metrics, in_train):
        self.metrics, self.in_train = listify(metrics), in_train

    def reset(self):
        self.tot_loss, self.count = 0.0, 0
        self.tot_mets = [0.0] * len(self.metrics)

    @property
    def all_stats(self):
        return [self.tot_loss.item()] + self.tot_mets

    @property
    def avg_stats(self):
        return [o / self.count for o in self.all_stats]

    def accumulate(self, run):
        bn = run.xb.shape[0]
        self.tot_loss += run.loss * bn
        self.count += bn
        for i, m in enumerate(self.metrics):
            self.tot_mets[i] += m(run.pred, run.yb) * bn

    def __repr__(self):
        if not self.count:
            return ""
        return f"{'train' if self.in_train else 'valid'}: {self.avg_stats}"


class AvgStatsCallBack(Callback):
    """
    AvgStatsCallBack class is a custom callback used to track and print average statistics for training and validation phases during the training loop.

    Arguments:
        metrics: A list of metric functions to evaluate during training and validation.

    Methods:
        __init__: Initializes the callback with given metrics and sets up AvgStats objects for both training and validation phases.
        begin_epoch: Resets the statistics at the beginning of each epoch.
        after_loss: Accumulates the metrics after computing the loss, differentiating between training and validation phases.
        after_epoch: Prints the accumulated statistics for both training and validation phases after each epoch.
    """
    def __init__(self, metrics):
        self.train_stats, self.valid_stats = AvgStats(metrics, True), AvgStats(
            metrics, False
        )

    def begin_epoch(self):
        self.train_stats.reset()
        self.valid_stats.reset()

    def after_loss(self):
        stats = self.train_stats if self.in_train else self.valid_stats
        with torch.no_grad():
            stats.accumulate(self.run)

    def after_epoch(self):
        print(self.train_stats)
        print(self.valid_stats)
    
