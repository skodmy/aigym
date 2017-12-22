"""
Defines a number of mixins which can be used for adding to dataset classes extra functionality.
"""
import os

from aigym.conf.settings import PREPARED_DATASETS_IMAGES_DIR, PREPARED_DATASETS_IMAGES_LABELS_DIR


class LabeledImagesMixin:
    """
    Mixin which can be used for dataset classes which are representable by labeled images.

    Defines corresponding properties.
    """
    def __init__(self):
        self._images = ()
        self._images_labels = ()

    @property
    def images(self):
        return self._images

    @images.setter
    def images(self, objects):
        self._images = objects

    @property
    def images_labels(self):
        return self._images_labels

    @images_labels.setter
    def images_labels(self, objects):
        self._images_labels = objects


class WithTestLabeledImagesMixin(LabeledImagesMixin):
    """
    Mixin which can be used for dataset classes which are representable by labeled images plus a test set.

    Defines corresponding properties.
    """
    def __init__(self):
        super().__init__()
        self._test_images = ()
        self._test_images_labels = ()

    @property
    def test_images(self):
        return self._test_images

    @test_images.setter
    def test_images(self, objects):
        self._test_images = objects

    @property
    def test_images_labels(self):
        return self._test_images_labels

    @test_images_labels.setter
    def test_images_labels(self, objects):
        self._test_images_labels = objects


class ConfigMixin:
    """
    Base class for config mixins.

    Main usage purpose is case when you need common config for both raw and prepared dataset classes.
    """
    filename = ''


class PreparedLabeledImagesConfigMixin(ConfigMixin):
    """
    LabeledImagesMixin corresponding config mixin class.
    """
    prepared_images_filename = ''
    prepared_images_labels_filename = ''


class WithTestPreparedLabeledImagesConfigMixin(PreparedLabeledImagesConfigMixin):
    """
    WithTestLabeledImagesMixin corresponding config mixin class.
    """
    prepared_test_images_filename = ''
    prepared_test_images_labels_filename = ''


class Fer2013DefaultConfigMixin(WithTestPreparedLabeledImagesConfigMixin):
    """
    fer2013 dataset default config mixin class.
    """
    filename = 'fer2013'
    prepared_images_filename = '{}_images.npy'.format(filename)
    prepared_images_labels_filename = '{}_images_labels.npy'.format(filename)
    prepared_test_images_filename = '{}_test_images.npy'.format(filename)
    prepared_test_images_labels_filename = '{}_test_images_labels.npy'.format(filename)
    prepared_private_test_images_filename = '{}_private_test_images.npy'.format(filename)
    prepared_private_test_images_labels_filename = '{}_private_test_images_labels.npy'.format(filename)
    filename += '.csv'
    face_size = 48
    emotion_choices = (
        'angry',
        'disgusted',
        'fearful',
        'happy',
        'sad',
        'surprised',
        'neutral',
    )
    prepared_images_filepath = os.path.join(PREPARED_DATASETS_IMAGES_DIR, prepared_images_filename)
    prepared_images_labels_filepath = os.path.join(PREPARED_DATASETS_IMAGES_LABELS_DIR, prepared_images_labels_filename)
    prepared_test_images_filepath = os.path.join(PREPARED_DATASETS_IMAGES_DIR, prepared_test_images_filename)
    prepared_test_images_labels_filepath = os.path.join(
        PREPARED_DATASETS_IMAGES_LABELS_DIR,
        prepared_test_images_labels_filename
    )
    prepared_private_test_images_filepath = os.path.join(
        PREPARED_DATASETS_IMAGES_DIR,
        prepared_private_test_images_filename
    )
    prepared_private_test_images_labels_filepath = os.path.join(
        PREPARED_DATASETS_IMAGES_LABELS_DIR,
        prepared_private_test_images_labels_filename
    )
