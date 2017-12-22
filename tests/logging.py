"""
Contains aigym.logging package tests.
"""
from unittest import TestCase

from aigym.conf.settings import DEBUG
from aigym.logging import logger
from aigym.logging.mixins import LoggerMixin


class LoggingTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logger_mixin = LoggerMixin()

    def test_logger_property(self):
        self.assertIsNotNone(self.logger_mixin.logger)

    def test_logger_handlers(self):
        logger_handlers_number = len(self.logger_mixin.logger.handlers)
        if DEBUG:
            self.assertEqual(logger_handlers_number, 2)
        else:
            self.assertEqual(logger_handlers_number, 1)

    def test_mixin_logger_and_global_logger_equality(self):
        self.assertEqual(self.logger_mixin.logger, logger)
