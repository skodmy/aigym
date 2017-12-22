"""
This module provides different configuration routines.

This routines can be used several times across the system.
"""
from typing import Union, Any, List, Tuple, Iterable
from inspect import ismodule


def extract_constants_from(source: Union[dict, Any]) -> List[Tuple[str, Any]]:
    """
    Extracts constants from a source.

    dict or module object can be passed as a source value.

    :return: list of (key, value) tuples.
    """
    if ismodule(source):
        source = source.__dict__
    return [item for item in source.items() if isinstance(item[0], str) and item[0].isupper()]


def print_constants_from(source: Iterable[Tuple[str, Any]]):
    """
    Prints constants from source.

    :param source: iterable of tuples which are kind of (str, any).
    """
    for key, value in source:
        print("{}={}".format(key, value))


def is_dir_const(name: str) -> bool:
    """
    Checks if provided constant name is a name of a directory constant.

    Returns True if the given constant name ends with '_DIR' substring, False otherwise.

    :param name: str object of constant name.
    :return: bool indicating that provided constant name is a name of directory constant.
    """
    return True if name.endswith('_DIR') else False


def get_dirs_constants_from(constants: Iterable[Tuple[str, Any]]) -> List[Tuple[str, Any]]:
    """
    Gets directory constants from a provided constants source.

    :param constants: iterable of (str, any) tuples.
    :return: list of (str, any) tuples where first item is directory constant name, second - its value.
    """
    return list(filter(lambda constant: is_dir_const(constant[0]), constants))


def get_dirs_constants_values_from(constants: Iterable[Tuple[str, Any]]) -> List[Any]:
    """
    Gets directory constants values from constants iterable.

    :param constants: iterable of (str, any) tuples.
    :return: list of any objects.
    """
    return [dir_const_value for _, dir_const_value in get_dirs_constants_from(constants)]
