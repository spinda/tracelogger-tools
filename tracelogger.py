#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.

import argparse
import functools

import tracelogger_clean
import tracelogger_run
import tracelogger_view

parser = argparse.ArgumentParser(
        description='Toolkit for working with SpiderMonkey\'s Tracelogger')

def print_help(argv, unknown):
    parser.print_help()
parser.set_defaults(func=print_help, parser=parser)

subparsers = parser.add_subparsers(help='sub-commands')
tracelogger_clean.command(
        functools.partial(subparsers.add_parser, 'clean'))
tracelogger_run.command(
        functools.partial(subparsers.add_parser, 'run'))
tracelogger_view.command(
        functools.partial(subparsers.add_parser, 'view'))

(argv, unknown) = parser.parse_known_args()
argv.func(argv, unknown)

