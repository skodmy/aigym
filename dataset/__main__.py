"""
usage: python -m aigym.dataset [-h] [-download url] [-prepare dataset name]

optional arguments:
  -h, --help                show this help message and exit
  -download url             download dataset file from url
  -prepare dataset name     prepares dataset specified by name
"""
import os
from argparse import ArgumentParser
from urllib.request import urlopen, urlsplit
from struct import pack

from tqdm import tqdm

import aigym.dataset
from aigym.conf.settings import RAW_DATASETS_DIR

arg_parser = ArgumentParser('aigym.dataset')
arg_parser.add_argument('-download', metavar='url', help="download dataset file from url")
arg_parser.add_argument('-prepare', metavar='dataset name', help="prepares dataset specified by name")

parsed_args = arg_parser.parse_args()

if parsed_args.download:
    source = urlopen(parsed_args.download)
    filename = os.path.split(urlsplit(parsed_args.download).path)[-1]
    with open(os.path.join(RAW_DATASETS_DIR, filename), 'wb') as file:
        for byte in tqdm(source.read(), desc='Downloading from {}'.format(parsed_args.download)):
            file.write(pack('B', byte))

if parsed_args.prepare:
    cls = getattr(aigym.dataset, "{}RawDataset".format(parsed_args.prepare.title()), None)
    if cls is not None:
        cls().prepare()
