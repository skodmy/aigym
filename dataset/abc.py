"""
Dataset base abstract classes module.
"""
from abc import ABC

from aigym.logging.mixins import LoggerMixin


class Dataset(LoggerMixin, ABC):
    """
    Dataset base abstract class.

    Stays on top of hierarchy.
    Defines base interface for dataset OOP representation.

    For your customization of dataset usage config property is provided.
    As a config value you can use object of any type, but you should know its interface for its usage in your code.
    """
    def __init__(self, config=None):
        self._config = None
        if config is not None:
            self.config = config

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, obj):
        self._config = obj


class RawDataset(Dataset):
    """
    Abstract base class for a dataset that contain raw data.

    Derived from Dataset class.
    Defines single method prepare which default implementation does nothing.
    """
    def prepare(self, *args, **kwargs):
        """
        Prepares raw dataset data for usage.

        You can pass needed arguments through *args and **kwargs.

        This implementation does nothing.
        """
        pass


class PreparedDataset(Dataset):
    """
    Abstract base class for ready for use datasets.

    Inherits from Dataset class.
    Defines single method load which default implementation does nothing.
    Have an ability of implicit loading of data by passing True to the __init__ method of self.
    """
    def __init__(self, config=None, load_implicitly: bool=True):
        """
        Initializes object with passed config and loads data implicitly if load_implicitly was True.

        If load_implicitly was False, then you will have to call load method yourself to actually load the data.
        :param config: any object.
        :param load_implicitly: a boolean flag that indicates load data here or not.
        """
        super().__init__(config)
        if load_implicitly:
            self.load()

    def load(self, *args, **kwargs):
        """
        Loads prepared dataset data.

        You can pass needed arguments through *args and **kwargs.

        This implementation does nothing.
        """
        pass
