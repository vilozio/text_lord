# -*- coding: utf-8 -*-
from pathlib import Path


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
            print('Can\'t read file {0}. Bad encoding.'
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
