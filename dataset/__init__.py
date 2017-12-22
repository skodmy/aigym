"""
Defines ready to use dataset classes.

They are placed here to make import statements more readable and short.
"""
from os import path
from typing import Tuple

from numpy import ndarray, zeros, uint8, fromstring, array, save, load
from cv2 import cvtColor, imdecode, COLOR_BGR2GRAY, IMREAD_GRAYSCALE, resize, INTER_CUBIC, error
from pandas import read_csv
from PIL.Image import fromarray
from tqdm import tqdm

from aigym.conf.settings import RAW_DATASETS_DIR

from .abc import RawDataset, PreparedDataset
from .classifiers import detect_face, FRONTALFACE_CASCADE_CLASSIFIER
from .mixins import Fer2013DefaultConfigMixin, WithTestLabeledImagesMixin


class Fer2013RawDataset(Fer2013DefaultConfigMixin, RawDataset):
    """
    OOP representation of fer2013 dataset with default config.
    """
    @staticmethod
    def wrap_with_gray_border(first_dimension: int, second_dimension: int, image):
        """
        Wraps image with a gray border.

        :param first_dimension: scalar value of first dimension.
        :param second_dimension: scalar value of second dimension.
        :param image: object to wrap.
        :return: wrapped image object.
        """
        double_first_dimension = first_dimension * 2
        gray_border = zeros([double_first_dimension, double_first_dimension], uint8)
        gray_border[:, :] = 200
        dimensions_sum = first_dimension + second_dimension
        dimensions_sub = first_dimension - second_dimension
        gray_border[dimensions_sub: dimensions_sum, dimensions_sub: dimensions_sum] = image
        return gray_border

    @staticmethod
    def gray_scale(image):
        """

        :param image:
        :return:
        """
        if len(image.shape) > 2 and image.shape[2] == 3:
            image = cvtColor(image, COLOR_BGR2GRAY)
        else:
            image = imdecode(image, IMREAD_GRAYSCALE)
        return image

    def format(self, image, wrap_with_gray_border=True):
        """
        Formats an image.

        Implemented algorithm contains next steps:
            1.Grayscales the image
            2.Wraps it with a gray border
            3.Detects face.
            4.Resizes due to config
            5.Return formatted image

        :param wrap_with_gray_border: boolean flag indication to wrap with gray border or not.
        :param image: image object.
        :return: formatted image.
        """
        image = self.gray_scale(image)

        if wrap_with_gray_border:
            image = self.wrap_with_gray_border(75, 24, image)

        image = detect_face(image, FRONTALFACE_CASCADE_CLASSIFIER)

        try:
            return resize(image, (self.face_size, self.face_size), interpolation=INTER_CUBIC) / 255
        except error:
            self.logger.warning("Error occurred during resizing in format of {}".format(self.__class__.__name__))
            return None

    def to_vector(self, emotion_scalar: int) -> ndarray:
        """
        Converts emotion scalar value to vector.

        :param emotion_scalar: emotion int value.
        :return: emotion value as numpy.ndarray.
        """
        result = zeros(len(self.emotion_choices))
        result[emotion_scalar] = 1.0
        return result

    def to_image(self, data):
        """
        Converts data to image.

        :param data: array of binary data
        :return: formatted image.
        """
        return self.format(
            array(
                fromarray(
                    fromstring(str(data), dtype=uint8, sep=' ').reshape((self.face_size, self.face_size))
                ).convert('RGB')
            )[:, :, ::-1].copy()
        )

    def images_and_labels_from(self, data_frame, progress_desc='') -> Tuple:
        """
        Extracts images and labels from data frame.

        :param data_frame: pandas.DataFrame object.
        :param progress_desc: message to show on left side from progress bar.
        :return: tuple of two values - images, labels.
        """
        images = []
        labels = []
        for _, row in tqdm(data_frame.iterrows(), desc=progress_desc):
            label = self.to_vector(row['emotion'])
            image = self.to_image(row['pixels'])
            if image is not None:
                images.append(image)
                labels.append(label)
            else:
                pass
        return images, labels

    def prepare(self, *args, **kwargs):
        """
        Prepares dataset.

        First extracts learning and test data from raw dataset file.
        Dataset filename is taken from self.filename.
        In the last step saves extracted data to corresponding files.
        Names of that files are defined in config mixin.
        """
        raw_data = read_csv(path.join(RAW_DATASETS_DIR, self.filename))

        images, images_labels = self.images_and_labels_from(
            raw_data.loc[raw_data['Usage'] == 'Training'], 'Converting training'
        )
        test_images, test_images_labels = self.images_and_labels_from(
            raw_data.loc[raw_data['Usage'] == 'PublicTest'], 'Converting test'
        )

        if kwargs.get('include_private_test', False):
            private_test_images, private_test_images_labels = self.images_and_labels_from(
                raw_data.loc[raw_data['Usage'] == 'PrivateTest'], 'Converting private test'
            )
            save(self.prepared_private_test_images_filepath, private_test_images)
            save(self.prepared_private_test_images_labels_filepath, private_test_images_labels)

        save(self.prepared_images_filepath, images)
        save(self.prepared_images_labels_filepath, images_labels)
        save(self.prepared_test_images_filepath, test_images)
        save(self.prepared_test_images_labels_filepath, test_images_labels)


class Fer2013PreparedDataset(Fer2013DefaultConfigMixin, WithTestLabeledImagesMixin, PreparedDataset):
    """
    OOP representation of ready to use fer2013 dataset with default config.

    Instantiated object doesn't contain data itself. For that purpose you need to call its load method.
    """
    def __init__(self, load_implicitly=False):
        PreparedDataset.__init__(self, Fer2013DefaultConfigMixin, load_implicitly)

    def load(self, *args, **kwargs):
        """
        Load prepared dataset data from files.

        Loaded data are stored in corresponding properties of self.
        Files names are defined in config mixin.
        """
        self.images = load(self.prepared_images_filepath)
        self.images_labels = load(self.prepared_images_labels_filepath)

        if kwargs.get('use_private_test', False):
            prepared_test_images_filepath = self.prepared_private_test_images_filepath
            prepared_test_images_labels_filepath = self.prepared_private_test_images_labels_filepath
        else:
            prepared_test_images_filepath = self.prepared_test_images_filepath
            prepared_test_images_labels_filepath = self.prepared_test_images_labels_filepath

        self.test_images = load(prepared_test_images_filepath)
        self.test_images_labels = load(prepared_test_images_labels_filepath)

        self.images = self.images.reshape([-1, self.face_size, self.face_size, 1])
        self.images_labels = self.images_labels.reshape([-1, len(self.emotion_choices)])

        self.test_images = self.test_images.reshape([-1, self.face_size, self.face_size, 1])
        self.test_images_labels = self.test_images_labels.reshape([-1, len(self.emotion_choices)])
