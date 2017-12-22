"""
This module provides convenience interface to cascade classifying.

FRONTALFACE_CASCADE_CLASSIFIER - instance of cv2.CascadeClassifier class for HAARCASCADE_FRONTALFACE_CLASSIFIER_FILEPATH

"""
import cv2

from aigym.conf.settings import HAARCASCADE_FRONTALFACE_CLASSIFIER_FILEPATH

FRONTALFACE_CASCADE_CLASSIFIER = cv2.CascadeClassifier(HAARCASCADE_FRONTALFACE_CLASSIFIER_FILEPATH)


def detect_face(image, classifier):
    """
    Detects a face on image by using cascade classifier.

    Chops image to face max area.

    :param image: source for face detection.
    :param classifier: cascade classifier object that will be used for face detection.
    :return: face image.
    """
    if image is None:
        return None
    faces = classifier.detectMultiScale(image, scaleFactor=1.3, minNeighbors=5)
    if not len(faces) > 0:
        return None
    max_area_face = faces[0]
    for face in faces:
        if face[2] * face[3] > max_area_face[2] * max_area_face[3]:
            max_area_face = face
    face = max_area_face
    return image[face[1]:(face[1] + face[2]), face[0]:(face[0] + face[3])]
