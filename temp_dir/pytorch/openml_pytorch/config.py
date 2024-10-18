#TODO: remove this somehow
from .trainer import OpenMLTrainerModule, OpenMLDataModule
import logging

data_module: OpenMLDataModule = OpenMLDataModule()
trainer: OpenMLTrainerModule = OpenMLTrainerModule(data_module=data_module)

global logger
# logger is the default logger for the PyTorch extension
logger = logging.getLogger(__name__)  # type: logging.Logger