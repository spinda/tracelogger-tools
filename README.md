# tracelogger-tools

This is a simple toolkit for working with SpiderMonkey's Tracelogger
debugging/profiling system.

## Installation

 1. Ensure `python3` is installed.
 2. Copy the contents of this repository wherever you like.
 3. Symlink `tracelogger.py` as `tracelogger` somewhere in your `$PATH`.

## Usage

The `tracelogger` command contains three handy subcommands. Run `tracelogger -h`
for usage information, or `tracelogger <subcommand> -h` for usage information
for a particular subcommand.

### `tracelogger clean`

Clears out all `tl-*.json` and `tl-*.tl` files left over from previous
Tracelogger runs. Use `-d`/`--directory` to manually specify a non-default
Tracelogger output directory. `-v`/`--verbose` prints out each file deleted, and
`-i`/`--interactive` asks for confirmation before deleting each file.

### `tracelogger run`

Run a command with the magic environment variables set to enable Tracelogger
output. Use `-l`/`--log` and `-o`/`--options` if you need to manually tweak
the values of these variables. Separate your command from your `tracelogger run`
options with `--`. For example:

```
tracelogger run -- js -e 'print("Hi!");'
tracelogger run -o Something,Special -- js -e 'print("Hi!");'
```

### `tracelogger save`

Collect Tracelogger output files in a directory and move them to a new one.

```
tracelogger save ~/traces/my-benchmark
```

Use `-d`/`--directory` to manually specify a non-default *source* directory, and
`-c`/`--copy` to copy the files instead of moving them. `-v`/`--verbose` turnson
verbose logging and `-i`/`--interactive` asks for confirmation before processing
each file.

### `tracelogger view`

Launch a local web server with a GUI viewer for your Tracelogger output. Use
`-o`/`--open` to auto-open the web page in a new browser tab, and
`-d`/`--directory` if you need to manually specify a non-default Tracelogger
output directory. `-t`/`--title` lets you set a custom title for the web viewer
page (useful when comparing multiple traces). `-a`/`--address` and `-p`/`--port`
let you specify a specific host address and port for the HTTP server, and
`-v`/`--verbose` prints out server request log information.

## License

tracelogger-tools is licensed under the Mozilla Public License, Version 2.0. The
text of this license can be found in the [LICENSE file](/LICENSE) and on its
[website](https://www.mozilla.org/en-US/MPL/2.0/). The
[FAQ](https://www.mozilla.org/en-US/MPL/2.0/FAQ/) may also be helpful.

The web UI is taken and slightly modified from
[h4writer/tracelogger](https://github.com/h4writer/tracelogger/).

