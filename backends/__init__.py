"""
Defines ready to use backend classes.
"""
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression

from aigym.dataset import Fer2013PreparedDataset

from .base import DNNBackend


def get_backend_class_by_name(value: str) -> type:
    """

    :param value:
    :return:
    """
    from sys import modules
    value = value if value.lower().endswith('backend') else "{}Backend".format(value.title())
    return getattr(modules[__name__], value, None)


class EmrecBackend(DNNBackend):
    """
     Emotion recognition backend class.

     Can be used for emotion recognition on images.
     Uses prepared fer2013 dataset for learning.
    """
    def __init__(self):
        """
        Initializing self with super.__init__() and prepared fer2013 OOP representation.
        """
        super().__init__()
        self.prepared_dataset = Fer2013PreparedDataset()

    def build_algorithm(self):
        """
        Builds architecture of emotion recognition DNN.
        """
        self.log_named('algorithm building started...')
        self.algorithm = input_data([None, self.prepared_dataset.face_size, self.prepared_dataset.face_size, 1])
        self.algorithm = conv_2d(self.algorithm, 64, 5, activation='relu')
        self.algorithm = max_pool_2d(self.algorithm, 3, strides=2)
        self.algorithm = conv_2d(self.algorithm, 64, 5, activation='relu')
        self.algorithm = max_pool_2d(self.algorithm, 3, strides=2)
        self.algorithm = conv_2d(self.algorithm, 128, 4, activation='relu')
        self.algorithm = dropout(self.algorithm, 0.3)
        self.algorithm = fully_connected(self.algorithm, 3072, activation='relu')
        self.algorithm = fully_connected(self.algorithm, len(self.prepared_dataset.emotion_choices), activation='softmax')
        self.algorithm = regression(self.algorithm, optimizer='momentum', loss='categorical_crossentropy')
        self.log_named('algorithm building finished.')

    def learn_model(self):
        """
        Learns model on prepared fer2013 dataset by using its fit method.
        """
        self.log_named('model learning started')
        self.prepared_dataset.load(use_private_test=True)
        if self.model is not None:
            self.model.fit(
                self.prepared_dataset.images, self.prepared_dataset.images_labels,
                validation_set=(self.prepared_dataset.test_images, self.prepared_dataset.test_images_labels),
                n_epoch=100,
                batch_size=50,
                shuffle=True,
                show_metric=True,
                snapshot_step=200,
                snapshot_epoch=True,
                run_id="{}Net".format(self.name),
            )
            self.log_named('model learning finished')
        else:
            self.log_named_warning('model learning failed, because model is None!')

    def respond_on(self, request):
        """
        Uses model to predict emotion on face image.

        :param request: image object.
        :return: prediction result.
        """
        if request is None:
            return None
        return self.model.predict(
            request.reshape([-1, self.prepared_dataset.face_size, self.prepared_dataset.face_size, 1])
        )
