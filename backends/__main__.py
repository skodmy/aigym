"""
Provides command-line interface to backends of aigym.

usage: python -m aigym.backends [-h] [-visualize backend name] [-train backend name] [-restore--training backend name]

optional arguments:
  -h, --help                        show this help message and exit
  -visualize backend name           visualize with tensorboard model of backend with a name 'name'
  -train backend name               train model of backend with a name 'name'
  -restore--training backend name   restore model learning of backend with a name 'name'

"""
from argparse import ArgumentParser
from subprocess import run

from aigym.backends import get_backend_class_by_name
from aigym.backends.plots import plot_emrecbackend_model_prediction_matrix


argument_parser = ArgumentParser('aigym backends')
argument_parser.add_argument(
    '-visualize',
    metavar='backend name',
    help="visualize with tensorboard model of backend with a name 'name'",
)
argument_parser.add_argument(
    '-train',
    metavar='backend name',
    help="train model of backend with a name 'name'",
)
argument_parser.add_argument(
    '-restore--training',
    metavar='backend name',
    help="restore model learning of backend with a name 'name'",
)
argument_parser.add_argument(
    '-plot',
    action='store_true',
    help="plots model prediction matrix using pyplot from matplotlib",
)

parsed_arguments = argument_parser.parse_args()


if parsed_arguments.visualize:
    backend_class = get_backend_class_by_name(parsed_arguments.visualize)
    if backend_class is not None:
        try:
            run(['tensorboard', '--logdir={}'.format(backend_class().learn_logs_dir_path)])
        except KeyboardInterrupt:
            exit()

if parsed_arguments.train:
    backend_class = get_backend_class_by_name(parsed_arguments.train)
    if backend_class is not None:
        backend = backend_class()
        backend.build_algorithm()
        backend.create_model()
        backend.learn_model()
        backend.save_model()

if parsed_arguments.restore__training:
    backend_class = get_backend_class_by_name(parsed_arguments.restore__training)
    if backend_class is not None:
        backend = backend_class()
        backend.build_algorithm()
        backend.create_model()
        backend.restore_model_learning()

if parsed_arguments.plot:
    plot_emrecbackend_model_prediction_matrix()
