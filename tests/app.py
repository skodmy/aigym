"""
Contains aigym.app package dummy tests :)
"""
from unittest import TestCase
from collections import deque

from aigym.app import AIApplication, BackendedAIApplication
from aigym.app.structure import DequeValuesDict, ApplicationStructureTemplate


class AIAppTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.obj = AIApplication()


class BackendedAIAppTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.backended_ai_app = BackendedAIApplication()

    def test_init(self):
        self.assertIsNone(self.backended_ai_app.backend)

    def test_backend(self):
        self.backended_ai_app.backend = 1
        self.assertIsNotNone(self.backended_ai_app.backend)


class DequeValuesDictTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.deque_values_dict = DequeValuesDict()

    def test_set_item(self):
        self.deque_values_dict[0] = 1
        self.assertIsInstance(self.deque_values_dict[0], deque)

    def test_missing(self):
        self.assertIsInstance(self.deque_values_dict[1], deque)


class AppStructTemplateTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app_struct_template = ApplicationStructureTemplate()

    def test_del_item(self):
        del self.app_struct_template[self.app_struct_template.tests_filename]
        self.assertIn(self.app_struct_template.tests_filename, self.app_struct_template)

    def test_tests_filename_property(self):
        self.assertEqual(self.app_struct_template.tests_filename, 'tests.py')
