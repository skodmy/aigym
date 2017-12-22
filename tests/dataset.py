"""
Contains aigym.dataset package tests.
"""
import os

from unittest import TestCase, skipUnless

from aigym.dataset import Fer2013RawDataset, Fer2013PreparedDataset
from aigym.dataset.classifiers import FRONTALFACE_CASCADE_CLASSIFIER, detect_face


class Fer2013DatasetTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fer2013_raw_dataset = Fer2013RawDataset()
        cls.fer2013_prepared_dataset = Fer2013PreparedDataset()
        cls.fer2013_raw_dataset.prepare()

    def test_prepare(self):
        self.assertTrue(
            all(
                (
                    os.path.exists(path_value)
                    for path_name, path_value in self.fer2013_raw_dataset.__dict__.items()
                    if path_name.endswith('_filepath')
                )
            )
        )

    def test_load(self):
        self.fer2013_prepared_dataset.load()
        self.assertTrue(
            all(
                True if len(attribute_value) != 0 else False
                for attribute_name, attribute_value in self.fer2013_prepared_dataset.__dict__.items()
                if attribute_name.startswith('test_images') or attribute_name.startswith('images_')
            )
        )


class DatasetClassifiersModuleTestCase(TestCase):
    def test_detect_face(self):
        self.assertIsNone(detect_face(None, FRONTALFACE_CASCADE_CLASSIFIER))
