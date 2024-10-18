"""
This module provides classes and methods to facilitate the configuration, data handling, training, and evaluation of machine learning models using PyTorch and OpenML datasets. The functionalities include:
- Generation of default configurations for models.
- Handling of image and tabular data.
- Training and evaluating machine learning models.
- Exporting trained models to ONNX format.
- Managing data transformations and loaders.
"""

import gc
import logging
import re
from types import SimpleNamespace
import warnings
import numpy as np
import torch
from typing import Any, Iterable, List, Optional, Tuple, Union
from collections import OrderedDict
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from openml.tasks import (
    OpenMLTask,
    OpenMLSupervisedTask,
    OpenMLClassificationTask,
    OpenMLRegressionTask,
)
import torch.amp
import pandas as pd
import copy
import io
import onnx
import torch.utils
from tqdm import tqdm
from .custom_datasets import OpenMLImageDataset, OpenMLTabularDataset
from openml.exceptions import PyOpenMLError
from types import SimpleNamespace
import matplotlib.pyplot as plt
from functools import partial
import math
from .callbacks import *
from .metrics import accuracy, accuracy_topk
from torchvision.transforms import Compose, Resize, ToPILImage, ToTensor, Lambda
from abc import ABC, abstractmethod


def convert_to_rgb(image):
    """
        Converts an image to RGB mode if it is not already in that mode.

        Parameters:
        image (PIL.Image): The image to be converted.

        Returns:
        PIL.Image: The converted image in RGB mode.
    """
    if image.mode != "RGB":
        return image.convert("RGB")
    return image

class DefaultConfigGenerator:
    """
    DefaultConfigGenerator class provides various methods to generate default configurations.
    """

    @staticmethod
    def _default_criterion_gen(task: OpenMLTask) -> torch.nn.Module:
        """
        _default_criterion_gen returns a criterion based on the task type - regressions use
        torch.nn.SmoothL1Loss while classifications use torch.nn.CrossEntropyLoss
        """
        if isinstance(task, OpenMLRegressionTask):
            return torch.nn.SmoothL1Loss()
        elif isinstance(task, OpenMLClassificationTask):
            return torch.nn.CrossEntropyLoss()
        else:
            raise ValueError(task)

    @staticmethod
    def _default_optimizer_gen(model: torch.nn.Module, _: OpenMLTask):
        """
        _default_optimizer_gen returns the torch.optim.Adam optimizer for the given model
        """
        return torch.optim.Adam

    @staticmethod
    def _default_scheduler_gen(optim, _: OpenMLTask) -> Any:
        """
        _default_scheduler_gen returns the torch.optim.lr_scheduler.ReduceLROnPlateau scheduler for the given optimizer
        """
        return torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer=optim)

    @staticmethod
    def _default_predict(output: torch.Tensor, task: OpenMLTask) -> torch.Tensor:
        """
        _default_predict turns the outputs into predictions by returning the argmax of the output tensor for classification tasks, and by flattening the prediction in case of the regression
        """
        output_axis = output.dim() - 1
        if isinstance(task, OpenMLClassificationTask):
            output = torch.argmax(output, dim=output_axis)
        elif isinstance(task, OpenMLRegressionTask):
            output = output.view(-1)
        else:
            raise ValueError(task)
        return output

    @staticmethod
    def _default_predict_proba(
        output: torch.Tensor, task: OpenMLTask
    ) -> torch.Tensor:
        """
        _default_predict_proba turns the outputs into probabilities using softmax
        """
        output_axis = output.dim() - 1
        output = output.softmax(dim=output_axis)
        return output

    @staticmethod
    def _default_sanitize(tensor: torch.Tensor) -> torch.Tensor:
        """
        _default sanitizer replaces NaNs with 1e-6
        """
        tensor = torch.where(
            torch.isnan(tensor), torch.ones_like(tensor) * torch.tensor(1e-6), tensor
        )
        return tensor

    @staticmethod
    def _default_retype_labels(
         tensor: torch.Tensor, task: OpenMLTask
    ) -> torch.Tensor:
        """
        _default_retype_labels changes the type of the tensor to long for classification tasks and to float for regression tasks
        """
        if isinstance(task, OpenMLClassificationTask):
            return tensor.long()
        elif isinstance(task, OpenMLRegressionTask):
            return tensor.float()
        else:
            raise ValueError(task)

    def get_device(
        self,
    ):
        """
        Checks if a GPU is available and returns the device to be used for training (cuda, mps or cpu)
        """
        if torch.cuda.is_available():
            device = torch.device("cuda")
        elif torch.backends.mps.is_available() and torch.backends.mps.is_built():
            device = torch.device("mps")
        else:
            device = torch.device("cpu")

        return device

    def default_image_transform(self):
        return Compose(
            [
                ToPILImage(),  # Convert tensor to PIL Image to ensure PIL Image operations can be applied.
                Lambda(convert_to_rgb),  # Convert PIL Image to RGB if it's not already.
                Resize((128, 128)),  # Resize the image.
                ToTensor(),  # Convert the PIL Image back to a tensor.
            ]
        )

    def return_model_config(self):
        """
        Returns a configuration object for the model
        """

        return SimpleNamespace(
            device=self.get_device(),
            criterion=self._default_criterion_gen,
            optimizer_gen=self._default_optimizer_gen,
            scheduler_gen=self._default_scheduler_gen,
            # predict turns the outputs of the model into actual predictions
            predict=self._default_predict,  # type: Callable[[torch.Tensor, OpenMLTask], torch.Tensor]
            # predict_proba turns the outputs of the model into probabilities for each class
            predict_proba=self._default_predict_proba,  # type: Callable[[torch.Tensor], torch.Tensor]
            # epoch_count represents the number of epochs the model should be trained for
            epoch_count=3,  # type: int,
            # progress_callback=(
            #     self._default_progress_callback
            # ),  # type: Callable[[int, int, int, int, float, float], None]
            # enable progress bar
            verbose=True,
        )

    def return_data_config(self):
        """
        Returns a configuration object for the data
        """
        return SimpleNamespace(
            type_of_data="image",
            perform_validation=False,
            # progress_callback is called when a training step is finished, in order to report the current progress
            # sanitize sanitizes the input data in order to ensure that models can be trained safely
            sanitize=self._default_sanitize,  # type: Callable[[torch.Tensor], torch.Tensor]
            # retype_labels changes the types of the labels in order to ensure type compatibility
            retype_labels=(
                self._default_retype_labels
            ),  # type: Callable[[torch.Tensor, OpenMLTask], torch.Tensor]
            # image_size is the size of the images that are fed into the model
            image_size=128,
            # batch_size represents the processing batch size for training
            batch_size=64,  # type: int
            data_augmentation=None,
            validation_split=0.1,
            transform=self.default_image_transform(),
        )


class BaseDataHandler:
    """
        BaseDataHandler class is an abstract base class for data handling operations.
    """
    def prepare_data(self, X_train, y_train, X_val, y_val, data_config=None):
        raise NotImplementedError

    def prepare_test_data(self, X_test, data_config=None):
        raise NotImplementedError


class OpenMLImageHandler(BaseDataHandler):
    """
        OpenMLImageHandler is a class that extends BaseDataHandler to handle image data from OpenML datasets.
    """
    def prepare_data(self, X_train, y_train, X_val, y_val, data_config = None):
        train = OpenMLImageDataset(
            image_dir=data_config.file_dir,
            X=X_train,
            y=y_train,
            transform_x=data_config.transform,
            image_size=data_config.image_size,
        )
        val = OpenMLImageDataset(
            image_dir=data_config.file_dir,
            X=X_val,
            y=y_val,
            transform_x=data_config.transform,
            image_size=data_config.image_size,
        )
        return train, val

    def prepare_test_data(self, X_test, data_config = None):
        test = OpenMLImageDataset(
            image_dir=data_config.file_dir,
            X=X_test,
            y=None,
            transform_x=data_config.transform,
            image_size=data_config.image_size,
        )
        return test


class OpenMLTabularHandler(BaseDataHandler):
    """
    OpenMLTabularHandler is a class that extends BaseDataHandler to handle tabular data from OpenML datasets.
    """
    def prepare_data(self, X_train, y_train, X_val, y_val, data_config = None):
        train = OpenMLTabularDataset(X=X_train, y=y_train)
        val = OpenMLTabularDataset(X=X_val, y=y_val)
        return train, val

    def prepare_test_data(self, X_test, data_config = None):
        test = OpenMLTabularDataset(X=X_test, y=None)
        return test


# Dictionary mapping data types to handlers
data_handlers = {
    "image": OpenMLImageHandler(),
    "dataframe": OpenMLTabularHandler(),
    # Add new data types here
}


class DataContainer:
    """
    class DataContainer:
        A class to contain the training, validation, and test data loaders. This just makes it easier to access them when required.

        Attributes:
        train_dl: DataLoader object for the training data.
        valid_dl: DataLoader object for the validation data.
        test_dl: Optional DataLoader object for the test data.
    """
    def __init__(self, train_dl, valid_dl, test_dl=None):
        self.train_dl, self.valid_dl = train_dl, valid_dl
        self.test_dl = test_dl

    @property
    def train_ds(self):
        return self.train_dl.dataset

    @property
    def valid_ds(self):
        return self.valid_dl.dataset

    @property
    def test_ds(self):
        return self.test_dl.dataset


class OpenMLDataModule:
    def __init__(
        self,
        type_of_data="image",
        filename_col="Filename",
        file_dir="images",
        target_mode="categorical",
        transform=None,
        target_column="encoded_labels",
        **kwargs,
    ):
        self.config_gen = DefaultConfigGenerator()
        self.data_config = self.config_gen.return_data_config()
        self.data_config.type_of_data = type_of_data
        self.data_config.filename_col = filename_col
        self.data_config.file_dir = file_dir
        self.data_config.target_mode = target_mode
        self.data_config.target_column = target_column
        self.handler = data_handlers.get(type_of_data)

        if transform is not None:
            self.data_config.transform = transform

        if not self.handler:
            raise ValueError(f"Data type {type_of_data} not supported.")

    def get_data(
        self,
        X_train: pd.DataFrame,
        y_train: Optional[pd.Series],
        X_test: pd.DataFrame,
        task,
    ):
        # Split the training data
        if type(y_train) != pd.Series:
            y_train = pd.Series(y_train)

        X_train_train, X_val, y_train_train, y_val = train_test_split(
            X_train,
            y_train,
            test_size=self.data_config.validation_split,
            shuffle=True,
            stratify=y_train,
            random_state=0,
        )

        # Encode the labels for categorical data
        if self.data_config.target_mode == "categorical":
            label_encoder = preprocessing.LabelEncoder().fit(y_train_train)
            y_train_train = pd.Series(label_encoder.transform(y_train_train))
            y_val = pd.Series(label_encoder.transform(y_val))
            # Determine model classes
            model_classes = (
                label_encoder.classes_
                if self.data_config.target_mode == "categorical"
                else None
            )
        
        # if self.data_config.type_of_data == "dataframe":
        #     # convert string columns to categorical columns
        #     

        # Use handler to prepare datasets
        train, val = self.handler.prepare_data(
            X_train_train, y_train_train, X_val, y_val, self.data_config
        )

        # Create DataLoaders
        train_loader = torch.utils.data.DataLoader(
            train, batch_size=self.data_config.batch_size, shuffle=True
        )
        val_loader = torch.utils.data.DataLoader(
            val, batch_size=self.data_config.batch_size, shuffle=False
        )

        # Prepare test data
        test = self.handler.prepare_test_data(X_test, self.data_config)
        test_loader = torch.utils.data.DataLoader(
            test, batch_size=self.data_config.batch_size, shuffle=False
        )

        return DataContainer(train_loader, val_loader, test_loader), model_classes


class ModelRunner:
    def __init__(self, cbs=None, cb_funcs=None):
        cbs = listify(cbs)
        for cbf in listify(cb_funcs):
            cb = cbf()
            setattr(self, cb.name, cb)
            cbs.append(cb)
        self.stop, self.cbs = False, [TrainEvalCallback()] + cbs

    @property
    def opt(self):
        return self.learn.opt

    @property
    def model(self):
        return self.learn.model

    @property
    def criterion(self):
        return self.learn.criterion

    @property
    def data(self):
        return self.learn.data

    @property
    def label_mapping(self):
        return self.learn.label_mapping

    @property
    def model_classes(self):
        return self.learn.model_classes

    def one_batch(self, xb, yb):
        try:
            self.xb, self.yb = xb, yb
            self.xb = self.xb.to(self.learn.device)
            self.yb = self.yb.to(self.learn.device)
            # Below two lines are hack to convert model to onnx
            global sample_input
            sample_input = self.xb
            self("begin_batch")
            self.pred = self.model(self.xb)
            self("after_pred")
            self.loss = self.criterion(self.pred, self.yb)
            self("after_loss")
            if not self.in_train:
                return
            self.loss.backward()
            self("after_backward")
            self.opt.step()
            self("after_step")
            self.opt.zero_grad()
        except CancelBatchException:
            self("after_cancel_batch")
        finally:
            self("after_batch")

    def all_batches(self, dl):
        self.iters = len(dl)
        try:
            for xb, yb in tqdm(dl, leave=False):
                self.one_batch(xb, yb)
        except CancelEpochException:
            self("after_cancel_epoch")

    def fit(self, epochs, learn):
        self.epochs, self.learn, self.loss = epochs, learn, torch.tensor(0.0)
        try:
            for cb in self.cbs:
                cb.set_runner(self)
            self("begin_fit")
            for epoch in range(epochs):
                self.epoch = epoch
                if not self("begin_epoch"):
                    self.all_batches(self.data.train_dl)
                with torch.no_grad():
                    if not self("begin_validate"):
                        self.all_batches(self.data.valid_dl)
                self("after_epoch")
        except CancelTrainException:
            self("after_cancel_train")
        finally:
            self("after_fit")
            self.learn = None

    def __call__(self, cb_name):
        res = False
        for cb in sorted(self.cbs, key=lambda x: x._order):
            res = cb(cb_name) and res
        return res


class Learner:
    def __init__(self, model, opt, criterion, data, model_classes):
        (
            self.model,
            self.opt,
            self.criterion,
            self.data,
            self.model_classes,
        ) = (model, opt, criterion, data, model_classes)


class OpenMLTrainerModule:

    def _default_progress_callback(
        self, fold: int, rep: int, epoch: int, step: int, loss: float, accuracy: float
    ):
        # todo : move this into callback
        """
                _default_progress_callback reports the current fold, rep, epoch, step and loss for every
        training iteration to the default logger
        """
        self.logger.info(
            "[%d, %d, %d, %d] loss: %.4f, accuracy: %.4f"
            % (fold, rep, epoch, step, loss, accuracy)
        )
    def __init__(
        self,
        data_module: OpenMLDataModule,
        callbacks: List[Callback] = [],
        **kwargs,
    ):
        self.config_gen = DefaultConfigGenerator()
        self.model_config = self.config_gen.return_model_config()
        self.data_module = data_module
        self.callbacks = callbacks

        self.config = SimpleNamespace(
            **{**self.model_config.__dict__, **self.data_module.data_config.__dict__}
        )
        # update the config with the user defined values
        self.config.__dict__.update(kwargs)
        self.config.progress_callback = self._default_progress_callback
        self.logger: logging.Logger = logging.getLogger(__name__)

        self.user_defined_measures = OrderedDict()
        # self.callbacks.append(LoggingCallback(self.logger, print_output=False))
        self.loss = 0
        self.training_state = True

        self.phases = [0.2, 0.8]
        self.scheds = combine_scheds(
            self.phases, [sched_cos(1e-4, 5e-3), sched_cos(5e-3, 1e-3)]
        )

        self.cbfs = [
            Recorder,
            partial(AvgStatsCallBack, [accuracy]),
            partial(ParamScheduler, "lr", self.scheds),
            # TensorBoardCallback(),
        ]

    def _onnx_export(self, model_copy):
        f = io.BytesIO()
        torch.onnx.export(model_copy, sample_input, f)
        onnx_model = onnx.load_model_from_string(f.getvalue())
        onnx_ = onnx_model.SerializeToString()
        return onnx_

    def run_model_on_fold(
        self,
        model: torch.nn.Module,
        task: OpenMLTask,
        X_train: pd.DataFrame,
        rep_no: int,
        fold_no: int,
        y_train: Optional[pd.Series],
        X_test: pd.DataFrame,
    ) -> Tuple[np.ndarray, Optional[np.ndarray], OrderedDict, Optional[Any]]:

        # if task has no class labels, we assign the class labels to be the unique values in the training set
        if task.class_labels is None:
            task.class_labels = y_train.unique()

        self.add_callbacks()

        self.model = copy.deepcopy(model)
        
        try:
            data, model_classes = self.run_training(task, X_train, y_train, X_test)

        except AttributeError as e:
            # typically happens when training a regressor8 on classification task
            raise PyOpenMLError(str(e))

        # In supervised learning this returns the predictions for Y
        pred_y, proba_y = self.run_evaluation(task, data, model_classes)

        # Convert predictions to class labels
        if task.class_labels is not None:
            pred_y = [task.class_labels[i] for i in pred_y]

        # Convert model to onnx
        onnx_ = self._onnx_export(self.model)

        global last_models
        last_models = onnx_

        return pred_y, proba_y, self.user_defined_measures, None

    def check_config(self):
        raise NotImplementedError

    def _prediction_to_probabilities(
        self, y: np.ndarray, classes: List[Any]
    ) -> np.ndarray:
        """Transforms predicted probabilities to match with OpenML class indices.

        Parameters
        ----------
        y : np.ndarray
            Predicted probabilities (possibly omitting classes if they were not present in the
            training data).
        model_classes : list
            List of classes known_predicted by the model, ordered by their index.

        Returns
        -------
        np.ndarray
        """
        # y: list or numpy array of predictions
        # model_classes: mapping from original array id to
        # prediction index id
        if not isinstance(classes, list):
            raise ValueError(
                "please convert model classes to list prior to " "calling this fn"
            )
        result = np.zeros((len(y), len(classes)), dtype=np.float32)
        for obs, prediction_idx in enumerate(y):
            result[obs][prediction_idx] = 1.0
        return result

    def run_evaluation(self, task, data, model_classes):
        if isinstance(task, OpenMLSupervisedTask):
            self.model.eval()
            pred_y = self.pred_test(task, self.model, data.test_dl, self.config.predict)
        else:
            raise ValueError(task)

        if isinstance(task, OpenMLClassificationTask):
            try:
                self.model.eval()
                proba_y = self.pred_test(
                    task, self.model, data.test_dl, self.config.predict_proba
                )

            except AttributeError:
                if task.class_labels is not None:
                    proba_y = self._prediction_to_probabilities(
                        pred_y, list(task.class_labels)
                    )
                else:
                    raise ValueError("The task has no class labels")

            if task.class_labels is not None:
                if proba_y.shape[1] != len(task.class_labels):
                    # Remap the probabilities in case there was a class missing
                    # at training time. By default, the classification targets
                    # are mapped to be zero-based indices to the actual classes.
                    # Therefore, the model_classes contain the correct indices to
                    # the correct probability array. Example:
                    # classes in the dataset: 0, 1, 2, 3, 4, 5
                    # classes in the training set: 0, 1, 2, 4, 5
                    # then we need to add a column full of zeros into the probabilities
                    # for class 3 because the rest of the library expects that the
                    # probabilities are ordered the same way as the classes are ordered).
                    proba_y_new = np.zeros((proba_y.shape[0], len(task.class_labels)))
                    for idx, model_class in enumerate(model_classes):
                        proba_y_new[:, model_class] = proba_y[:, idx]
                    proba_y = proba_y_new

                if proba_y.shape[1] != len(task.class_labels):
                    message = "Estimator only predicted for {}/{} classes!".format(
                        proba_y.shape[1],
                        len(task.class_labels),
                    )
                    warnings.warn(message)
                    self.logger.warning(message)
            else:
                raise ValueError("The task has no class labels")

        elif isinstance(task, OpenMLRegressionTask):
            proba_y = None

        else:
            raise TypeError(type(task))
        return pred_y, proba_y

    def run_training(self, task, X_train, y_train, X_test):
        if isinstance(task, OpenMLSupervisedTask) or isinstance(
            task, OpenMLClassificationTask
        ):
            self.opt = self.config.optimizer_gen(self.model, task)(
                self.model.parameters()
            )

            self.criterion = self.config.criterion(task)
            self.device = self.config.device

            if self.config.device != "cpu":
                self.criterion = self.criterion.to(self.config.device)

            data, model_classes = self.data_module.get_data(
                X_train, y_train, X_test, task
            )
            self.learn = Learner(
                self.model,
                self.opt,
                self.criterion,
                data,
                model_classes,
            )
            self.learn.device = self.device
            self.learn.model.to(self.device)
            gc.collect()

            self.runner = ModelRunner(cb_funcs=self.cbfs)
            self.learn.model.train()
            self.runner.fit(epochs=self.config.epoch_count, learn=self.learn)
            self.learn.model.eval()

            print("Loss", self.runner.loss)
        return data, model_classes

    def add_callbacks(self):
        if self.callbacks is not None and len(self.callbacks) > 0:
            for callback in self.callbacks:
                if callback not in self.cbfs:
                    self.cbfs.append(callback)

    def pred_test(self, task, model_copy, test_loader, predict_func):
        probabilities = []
        for batch_idx, inputs in enumerate(test_loader):
            inputs = self.config.sanitize(inputs)
            # if torch.cuda.is_available():
            inputs = inputs.to(self.config.device)

            # Perform inference on the batch
            pred_y_batch = model_copy(inputs)
            pred_y_batch = predict_func(pred_y_batch, task)
            pred_y_batch = pred_y_batch.cpu().detach().numpy()

            probabilities.append(pred_y_batch)

            # Concatenate probabilities from all batches
        pred_y = np.concatenate(probabilities, axis=0)
        return pred_y
