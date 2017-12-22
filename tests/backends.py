"""
Contains aigym.backends package tests.
"""
import os
from unittest import TestCase

from aigym.backends import EmrecBackend


class EmrecBackendTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.emrec_backend = EmrecBackend()
        cls.emrec_backend.build_algorithm()
        cls.emrec_backend.create_model()
        cls.emrec_backend.save_model()

    def test_build_algorithm(self):
        self.assertIsNotNone(self.emrec_backend.algorithm)

    def test_create_model(self):
        self.assertIsNotNone(self.emrec_backend.model)

    def test_save_model(self):
        self.assertNotEqual(os.listdir(self.emrec_backend.model_file_dir_path), 0)

    def test_load_model(self):
        self.emrec_backend.model.predictor = None
        self.emrec_backend.load_model()
        self.assertIsNotNone(self.emrec_backend.model.predictor)

    def test_respond_on(self):
        self.assertIsNone(self.emrec_backend.respond_on(None))

    # noinspection PyUnresolvedReferences
    @classmethod
    def tearDownClass(cls):
        for dir_item in os.listdir(cls.emrec_backend.model_file_dir_path):
            os.remove(os.path.join(cls.emrec_backend.model_file_dir_path, dir_item))
        del cls.emrec_backend
