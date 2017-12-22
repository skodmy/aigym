"""
This module defines logic that relates to application's structure.

The main class here is ApplicationStructureTemplate.
It defines application's file structure.
"""
from collections import abc, deque, UserDict
from typing import Any, Union, Iterable


class DequeValuesDict(UserDict):
    """
    This class defines a dict that wraps its values with a deque.
    """
    def __setitem__(self, key: Any, value: Union[Any, Iterable[Any]]):
        """
        Implementation of self[key] = value.

        :param key: any hashable object.
        :param value: any or iterable object.
        """
        super().__setitem__(key, deque((value, ) if not isinstance(value, abc.Iterable) else value))

    def __missing__(self, key: Any) -> deque:
        """
        Implementation of self[key].

        :param key: any hashable object.
        :return: value which is a deque instance.
        """
        return deque()


class ApplicationStructureTemplate(DequeValuesDict):
    """
    Class which instances describe applications structure template.
    """
    def __init__(self):
        super().__init__()
        self.update({
            '__init__.py': (
                "",
            ),
            'app.py': (
                "from aigym.app import BackendedAIApplication",
                "",
                "",
                "class App(BackendedAIApplication): pass",
                "",
            ),
            '__main__.py': (
                "from .app import App",
                "",
                "App().run()",
                "",
            ),
            self.tests_filename: (
                "from unittest import TestCase",
                "",
                "# write your app tests here",
                "",
                "if __name__ == 'main"
            ),
        })
        self.__must_have_files_names = tuple(self.keys())

    def __setitem__(self, key: str, value: Union[str, Iterable[str]]):
        """
        Implementation of self[key] = value.

        :param key: should be of str type or may be converted to it.
        :param value: should be of str type or iterable of str.
        """
        if not isinstance(key, str):
            key = str(key)
        if not isinstance(value, (str, Iterable)):
            value = str(value)
        if isinstance(value, Iterable):
            value = (item if isinstance(item, str) else str(item) for item in value)
        super().__setitem__(key, value)

    def __delitem__(self, key: str):
        """
        Implementation del self[key].

        Doesn't delete must have items.
        :param key: a string object.
        """
        if key not in self.__must_have_files_names:
            super().__delitem__(key)

    @property
    def must_have_files_names(self) -> tuple:
        """
        :return: tuple of must have files names.
        """
        return self.__must_have_files_names

    @property
    def tests_filename(self) -> str:
        """
        :return: application tests filename.
        """
        return 'tests.py'
