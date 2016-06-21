#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.

import argparse
import os
import sys

from glob import glob

def command(parser_base):
    parser = parser_base(
            description='Clean Tracelogger files from output directory')
    parser.add_argument('-d', '--directory',
            default=('.' if os.name == 'nt' else '/tmp'),
            help='Directory containing Tracelogger output (default: %(default)s)')
    parser.add_argument('-i', '--interactive',
            action='store_true',
            help='Ask for confirmation for each file deleted')
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
        target_dir = os.path.realpath(argv.directory)
        files = glob(os.path.join(target_dir, 'tl-*.json')) \
              + glob(os.path.join(target_dir, 'tl-*.tl'))
        files.sort()

        for f in files:
            if argv.interactive:
                sys.stdout.write('Delete {}? [y/N] '.format(f))
                choice = input().lower()
                if not choice.startswith('y'):
                    continue
            elif argv.verbose:
                print('deleting', f)
            os.remove(f)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    run(*command(argparse.ArgumentParser).parse_known_args())

