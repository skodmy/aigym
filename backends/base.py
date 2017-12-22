"""
Defines backend base class.
To define your own backend you need to inherit from this class.
"""
import os
from abc import ABC, abstractmethod
from typing import Any, Callable
from functools import partialmethod

from tflearn import DNN

from aigym.logging import logger
from aigym.logging.mixins import LoggerMixin
from aigym.conf.settings import CHECKPOINTS_BASE_DIR, LEARN_LOGS_BASE_DIR, MODELS_BASE_DIR, ASSETS_BASE_DIR


class BaseBackend(LoggerMixin, ABC):
    """
    Abstract base class for client code backend.
    """
    def __init__(self):
        self._algorithm = None
        self._model = None
        self._prepared_dataset = None
        self.setup()

    @property
    def algorithm(self):
        return self._algorithm

    @algorithm.setter
    def algorithm(self, obj):
        self._algorithm = obj

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, obj):
        self._model = obj

    @property
    def prepared_dataset(self):
        return self._prepared_dataset

    @prepared_dataset.setter
    def prepared_dataset(self, obj):
        self._prepared_dataset = obj

    @property
    def name(self):
        return self.__class__.__name__.replace('Backend', '')

    @property
    def model_filename(self):
        return "{}.model".format(self.name)

    @property
    def checkpoints_dir_path(self):
        return os.path.join(CHECKPOINTS_BASE_DIR, self.name)

    @property
    def learn_logs_dir_path(self):
        return os.path.join(LEARN_LOGS_BASE_DIR, self.name)

    @property
    def model_file_dir_path(self):
        return os.path.join(MODELS_BASE_DIR, self.name)

    @property
    def model_file_path(self):
        return os.path.join(self.model_file_dir_path, self.model_filename)

    def log_named(self, message: str, log_routine: Callable=None):
        """
        Logs named message by using log routine.

        Log routine is a callable from builtin logging module or Logger object from that module.
        As a log routine you should use one of self.logger methods.

        If log_routine is None then self.logger.debug.

        :param message: a str object which will be 'named' and then logged.
        :param log_routine: a callable that will be used for logging 'named' message.
        """
        if log_routine is None:
            log_routine = self.logger.debug
        if callable(log_routine):
            log_routine("{} {}".format(self.name, message))

    log_named_warning = partialmethod(log_named, log_routine=logger.warning)

    def setup(self):
        """
        Creates needed directories if they not exist.
        """
        if not os.path.exists(self.checkpoints_dir_path):
            os.mkdir(self.checkpoints_dir_path)
        if not os.path.exists(self.learn_logs_dir_path):
            os.mkdir(self.learn_logs_dir_path)
        if not os.path.exists(self.model_file_dir_path):
            os.mkdir(self.model_file_dir_path)

    @abstractmethod
    def build_algorithm(self):
        """
        Model algorithm must be built here.
        """
        raise NotImplementedError

    @abstractmethod
    def create_model(self):
        """
        Model must be created on a built algorithm here.
        """
        raise NotImplementedError

    @abstractmethod
    def learn_model(self):
        """
        Created model learning on a contained prepared dataset goes here.
        """
        raise NotImplementedError

    @abstractmethod
    def restore_model_learning(self):
        """
        Restoring of model learning goes here.
        """
        raise NotImplementedError

    @abstractmethod
    def save_model(self):
        """
        Learned model must be saved here.
        """
        raise NotImplementedError

    @abstractmethod
    def load_model(self) -> Any:
        """
        Saved model loading must be implemented here.

        :return: any object.
        """
        raise NotImplementedError

    @abstractmethod
    def respond_on(self, request: Any) -> Any:
        """
        Responds on a given request.

        :param request: any object.
        :return: any object.
        """
        raise NotImplementedError


# noinspection PyAbstractClass,PyCallingNonCallable
class DNNBackend(BaseBackend):
    def create_model(self):
        """
        Creates DNN model that is based on built algorithm.

        Needed algorithm is builded with self.build_algorithm call.
        """
        self.log_named("model creation started")
        if self.algorithm is not None:
            self.model = DNN(
                self.algorithm,
                checkpoint_path=self.checkpoints_dir_path,
                max_checkpoints=1,
                tensorboard_verbose=3,
                tensorboard_dir=self.learn_logs_dir_path
            )
            self.log_named("model creation finished")
        else:
            self.log_named_warning("model was not created, because algorithm is None!")

    def save_model(self):
        """
        Saves created DNN model to a file.

        Path to is got from self.model_file_path property.
        """
        if self.model is not None:
            self.model.save(self.model_file_path)
            self.log_named("model saved")
        else:
            self.log_named_warning("model file was not saved, because model is None!")

    def load_model(self):
        """
        Loads saved DNN model from a file.

        Path to is got from self.model_file_path property.
        """
        if self.model is not None:
            if os.path.exists(self.model_file_dir_path) and len(os.listdir(self.model_file_dir_path)):
                self.model.load(self.model_file_path)
                self.log_named("model loaded")
            else:
                self.log_named_warning("model file doesn't exist!")
        else:
            self.log_named_warning("model is None!")

    def restore_model_learning(self):
        """
        Restores model learning from the last checkpoint if such exists.
        """
        if self.model is not None:
            if os.path.exists(self.checkpoints_dir_path):
                with open(os.path.join(self.checkpoints_dir_path, 'checkpoint')) as checkpoint_file:
                    self.model.load(checkpoint_file.readline().split(': ')[-1][1:-2])
                    self.learn_model()
                    self.save_model()
            else:
                self.log_named_warning("checkpoints directory doesn't exist!")
        else:
            self.log_named_warning("can't restore model learning process, because model is None!")
