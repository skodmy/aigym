"""
This module provides aigym settings.

DEBUG - a boolean flag which indicates to turn on or off debugging stuff.

AIGYM_DIR - aigym package directory.

AIGYM_LOGFILE_FILENAME - aigym log file name, defaults to 'aigym.log'

HAARCASCADE_FILES_DIR - directory in which haarcascade files are placed.

DATASETS_BASE_DIR - directory in which datasets directories are located.

RAW_DATASETS_DIR - directory in which raw datasets files are placed.

PREPARED_DATASETS_DIR - directory in which prepared datasets directories are located and files are placed.

PREPARED_DATASETS_IMAGES_DIR - directory in which prepared datasets images files are placed.

PREPARED_DATASETS_IMAGES_LABELS_DIR - directory in which prepared datasets images labels files are placed.

CHECKPOINTS_BASE_DIR - directory in which directories of model checkpoints are placed.

LEARN_LOGS_BASE_DIR - directory in which directories of models learning logs are placed.

MODELS_BASE_DIR - directory where model files are saved or loaded from.

ASSETS_BASE_DIR - backends assets directories are placed there.

HAARCASCADE_FRONTALFACE_CLASSIFIER_FILEPATH - path to 'haarcascade_frontalface_default.xml' file.
"""
import os

DEBUG = True

AIGYM_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

AIGYM_LOGFILE_FILENAME = 'aigym.log'

HAARCASCADE_FILES_DIR = os.path.join(AIGYM_DIR, 'haarcascade_files')

DATASETS_BASE_DIR = os.path.join(AIGYM_DIR, 'datasets')

RAW_DATASETS_DIR = os.path.join(DATASETS_BASE_DIR, 'raw')

PREPARED_DATASETS_DIR = os.path.join(DATASETS_BASE_DIR, 'prepared')

PREPARED_DATASETS_IMAGES_DIR = os.path.join(PREPARED_DATASETS_DIR, 'images')

PREPARED_DATASETS_IMAGES_LABELS_DIR = os.path.join(PREPARED_DATASETS_DIR, 'labels')

CHECKPOINTS_BASE_DIR = os.path.join(AIGYM_DIR, 'checkpoints')

LEARN_LOGS_BASE_DIR = os.path.join(AIGYM_DIR, 'learn_logs')

MODELS_BASE_DIR = os.path.join(AIGYM_DIR, 'models')

ASSETS_BASE_DIR = os.path.join(AIGYM_DIR, 'assets')

HAARCASCADE_FRONTALFACE_CLASSIFIER_FILEPATH = os.path.join(HAARCASCADE_FILES_DIR, 'haarcascade_frontalface_default.xml')
