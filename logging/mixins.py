"""
Logging mixins lives here.
"""
import os
import logging

from aigym.conf import settings


class LoggerMixin:
    """
    Mixin which provides a derived class with a logger property.

    For logger defines two handlers:
        - file handler
        - stream handler
    File handler is used for logging warnings and errors and is always included.
    Stream handler is used for logging debug messages and is included only if aigym.conf.settings.DEBUG is set to True.

    If aigym.conf.settings.DEBUG is True then sets logger level to logging.DEBUG.
    """
    __logger = logging.getLogger('aigym logger')

    __formatter = logging.Formatter("[%(levelname)s][%(asctime)s]: aigym %(message)s")

    __file_handler = logging.FileHandler(os.path.join(settings.AIGYM_DIR, settings.AIGYM_LOGFILE_FILENAME))
    __file_handler.setLevel(logging.WARNING)
    __file_handler.setFormatter(__formatter)

    __logger.addHandler(__file_handler)

    if settings.DEBUG:
        __stream_handler = logging.StreamHandler()
        __stream_handler.setLevel(logging.DEBUG)
        __stream_handler.setFormatter(__formatter)

        __logger.addHandler(__stream_handler)
        __logger.setLevel(logging.DEBUG)

    @property
    def logger(self):
        return self.__logger
