"""
Contains aigym.conf package tests.
"""
from unittest import TestCase

from aigym.conf.routines import extract_constants_from, is_dir_const, get_dirs_constants_from
from aigym.conf.routines import get_dirs_constants_values_from


class ConfigurationRoutinesTestCase(TestCase):
    def test_extract_constants_from(self):
        self.assertEqual(len(extract_constants_from({})), 0)

    def test_is_dir_const(self):
        self.assertTrue(is_dir_const('SOME_ABSTRACT_DIR'))

    def test_get_dirs_constants_from(self):
        self.assertEqual(len(get_dirs_constants_from(tuple())), 0)

    def test_get_dirs_constant_values_from(self):
        self.assertEqual(len(get_dirs_constants_values_from(tuple())), 0)
