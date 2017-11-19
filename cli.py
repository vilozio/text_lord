# -*- coding: utf-8 -*-
"""Command line interface.
"""
import argparse
import os


class readable_resource(argparse.Action):
    def correct_resource(self, path):
        return os.path.isfile(path)

    def resource_type(self):
        return 'file'

    def __call__(self, parser, namespace, values, option_string=None):
        prospective_resource = values
        if not self.correct_resource(prospective_resource):
            raise argparse.ArgumentError(
                self,
                "{0} is not a valid path"
                .format(prospective_resource))
        if os.access(prospective_resource, os.R_OK):
            setattr(namespace, self.dest, prospective_resource)
        else:
            raise argparse.ArgumentError(
                self,
                "{0} is not a readable {1}"
                .format(prospective_resource, self.resource_type()))


class readable_file(readable_resource):
    def correct_resource(self, path):
        return os.path.isfile(path)

    def resource_type(self):
        return 'file'


class readable_dir(readable_resource):
    def correct_resource(self, path):
        return os.path.isdir(path)

    def resource_type(self):
        return 'dir'


def parse_args():
    """Parse args with argparse.

    Returns: Namespace args.
    """
    parser = argparse.ArgumentParser(
        description='A text lord that rules',
        epilog="And that's how you'd rule a text"
    )
    parser.add_argument('--log.conf', action=readable_file,
                        help='path to logging config file. YAML format is '
                             'supported only')
    parser.add_argument('-t', '--textrank', action='store_true',
                        help='doing special')
    parser.add_argument('-i', '--input', action=readable_dir,
                        help='input dir')
    parser.add_argument('-o', '--out', action=readable_dir,
                        help='output dir')
    parser.add_argument('--tree', action='store_true',
                        help='output as input dir tree')
    parser.add_argument('--separate', action='store_true',
                        help='output as input dir tree')
    # parser.add_argument('path', help='where data')
    args = parser.parse_args()
    return args
