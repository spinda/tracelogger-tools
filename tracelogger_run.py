#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.

import argparse
import os
import subprocess
import sys

class MyHelpFormatter(argparse.HelpFormatter):
    def format_help(self):
        help_text = super().format_help()
        help_lines = help_text.splitlines()
        help_lines[0] += ' -- COMMAND'
        help_lines.append(
                '  COMMAND               command to run with Tracelogger output enabled')
        help_lines.append('')
        return os.linesep.join(help_lines)

def command(parser_base):
    parser = parser_base(
            description='Run a command with Tracelogger output enabled',
            formatter_class=MyHelpFormatter)
    parser.add_argument('-l',  '--log',
            default='Default',
            help='comma-separated list of items to trace (default: %(default)s)')
    parser.add_argument('-o',  '--options',
            default='EnableMainThread,EnableOffThread,EnableGraph',
            help='comma-separated list of Tracelogger opts (default: %(default)s)')
    parser.set_defaults(func=run, parser=parser)
    return parser

def run(argv, cmd):
    if len(cmd) == 0 or cmd == ['--']:
        argv.parser.print_help()
        sys.exit()

    if cmd[0] == '--':
        cmd.pop(0)

    env = os.environ.copy()
    env["TLLOG"] = argv.log
    env["TLOPTIONS"] = argv.options

    try:
        sys.exit(subprocess.call(cmd, env=env))
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    run(*command(argparse.ArgumentParser).parse_known_args())

