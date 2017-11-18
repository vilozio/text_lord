# -*- coding: utf-8 -*-
import os
from pathlib import Path
from logging import getLogger

logger = getLogger(__name__)


def get_files_path(dir_path, pattern='**/*.txt'):
    paths = []
    pathlist = Path(dir_path).glob(pattern)
    for path in pathlist:
        paths.append(str(path))
    return paths


def read_file_text(filename, encoding='utf-8'):
    text = ''
    with open(filename, 'r', encoding=encoding) as f:
        try:
            text = f.read()
        except UnicodeDecodeError:
            logger.warning('Can\'t read file {0}. Bad encoding.'
                           .format(filename))
    return text


def loadAll(dir_path):
    text = ''
    for filename in get_files_path(dir_path):
        text = text + read_file_text(filename)
    return text


def load(dir_path):
    texts = {}
    for filename in get_files_path(dir_path):
        texts[filename] = read_file_text(filename)
    return texts


def save(path, text, encoding='utf-8'):
    dirs, filename = os.path.split(path)
    os.makedirs(dirs, exist_ok=True)
    with open(path, 'w', encoding=encoding) as f:
        f.write(text)


def rename_paths(paths, *patterns):
    new_paths = []
    for path in paths:
        for old, new in patterns:
            new_paths.append(path.replace(old, new))
    return new_paths
