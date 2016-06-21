#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.

import argparse
import os
import shutil
import sys

from glob import glob

def command(parser_base):
    parser = parser_base(
            description='Collect Tracelogger output files and move them to a new directory')
    parser.add_argument('new_directory',
            help='*New* directory to which the Tracelogger output files will be moved')
    parser.add_argument('-d', '--directory',
            default=('.' if os.name == 'nt' else '/tmp'),
            help='*Original* directory containing Tracelogger output (default: %(default)s)')
    parser.add_argument('-c', '--copy',
            action='store_true',
            help='Copy each file instead of moving')
    parser.add_argument('-i', '--interactive',
            action='store_true',
            help='Ask for confirmation for each file processed')
    parser.add_argument('-v', '--verbose',
            action='store_true',
            help='Enable verbose logging')
    parser.set_defaults(func=run, parser=parser)
    return parser

def run(argv, unknown):
    if len(unknown) != 0:
        argv.parser.print_usage()
        sys.exit()

    try:
        source_dir = os.path.realpath(argv.directory)
        target_dir = os.path.realpath(argv.new_directory)

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        files = glob(os.path.join(source_dir, 'tl-*.json')) \
              + glob(os.path.join(source_dir, 'tl-*.tl'))
        files.sort()

        for source_file in files:
            if argv.interactive:
                sys.stdout.write('{} {}? [y/N] '.format(
                        'Copy' if argv.copy else 'Move', source_file))
                choice = input().lower()
                if not choice.startswith('y'):
                    continue
            elif argv.verbose:
                print('{} {} to {}'.format(
                        'Copying' if argv.copy else 'Moving',
                        source_file, target_dir))
            if argv.copy:
                shutil.copy(source_file, target_dir)
            else:
                shutil.move(source_file, target_dir)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    run(*command(argparse.ArgumentParser).parse_known_args())

