#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.

import argparse
import http.server
import os
import re
import sys
import threading
import webbrowser

def command(parser_base):
    parser = parser_base(
            description='GUI viewer for Tracelogger output')
    parser.add_argument('-d', '--directory',
            default=('.' if os.name == 'nt' else '/tmp'),
            help='Directory containing Tracelogger output (default: %(default)s)')
    parser.add_argument('--open', action='store_true',
            help='Auto-open the Tracelogger viewer page in a new browser tab')
    parser.add_argument('-a', '--address',
            default='127.0.0.1',
            help='Address for the HTTP Server to listen on (default: %(default)s)')
    parser.add_argument('-p', '--port',
            default=0,
            help='Port for the HTTP server to listen on (default: random)')
    parser.add_argument('-v', '--verbose',
            action='store_true',
            help='Enable verbose logging')
    parser.set_defaults(func=run, parser=parser)
    return parser

def run(argv, unknown):
    if len(unknown) != 0:
        argv.parser.print_usage()
        sys.exit()

    tldir = os.path.realpath(argv.directory)
    uidir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ui')
    cwdir = os.getcwd()

    data_regex = re.compile(
            '^/data/tl-(data|dict|event|tree)(\.[0-9]+)*\.(json|tl)$')

    class RequestHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self, *args, **kwargs):
            try:
                if data_regex.match(self.path):
                    self.path = self.path[5:]
                    os.chdir(tldir)
                    super().do_GET(*args, **kwargs)
                else:
                    os.chdir(uidir)
                    super().do_GET(*args, **kwargs)
            finally:
                os.chdir(cwdir)

        def log_message(self, *args, **kwargs):
           if argv.verbose:
               super().log_message(*args, **kwargs)

    server_address = (argv.address, argv.port)
    httpd = http.server.HTTPServer(server_address, RequestHandler)

    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    web_address = 'http://{}:{}'.format(httpd.server_address[0],
                                        httpd.server_address[1])

    print('Server ready!')
    print('Visit {} in your web browser.'.format(web_address))
    print('(Press ^C to quit.)')

    if argv.open:
        webbrowser.open_new_tab(web_address)

    try:
        server_thread.join()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    run(*command(argparse.ArgumentParser).parse_known_args())

