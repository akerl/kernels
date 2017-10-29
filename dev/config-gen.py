#!/usr/bin/env python

import roller
import argparse
import os.path
import sys

def get_args(raw_args):
    parser = argparse.ArgumentParser(
        description='Generate a new kernel config'
    )
    parser.add_argument(
        '-k', '--kernel',
        dest='new_version',
        default=roller.get_latest_kernel_version('mainline'),
        help='Kernel version to build',
    )
    parser.add_argument(
        'config_file',
        help='Config file to work from',
    )
    parser.add_argument(
        '-b', '--build-dir',
        dest='build_dir',
        default='/tmp',
        help='directory for downloading, extracting, and building the kernel'
    )
    return parser.parse_args(raw_args)

def easy_config(raw_args):
    args = get_args(raw_args)

    config_abs_file = os.path.abspath(args.config_file)
    config_dir, config_full_version = os.path.split(config_abs_file)
    config_version, config_revision = config_full_version.split('_')

    kernel = roller.Kernel(
        build_dir=args.build_dir,
        config_dir=config_dir,
        verbose=True
    )

    kernel.version = args.new_version
    kernel.config_version = config_version
    kernel.config_revision = config_revision
    if args.new_version in kernel.existing_configs:
        last = max(kernel.existing_configs[args.new_version])
        kernel.revision = str(int(last) + 1)
    else:
        kernel.revision = '1'

    kernel.download()
    kernel.extract()
    kernel.configure()
    kernel.modify()

if __name__ == '__main__':
    easy_config(sys.argv[1:])