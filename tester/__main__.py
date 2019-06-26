"""
tester: unit and functional testing with Python.
"""

import argparse
import sys

from tester.commands import StartCommand, StatusCommand, RunCommand


def main():
    """ An entry point to dispatch commands. """
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="Tester commands")

    commands = [StartCommand(),
                StatusCommand(),
                RunCommand()]

    for command in commands:
        cmd_parser = subparsers.add_parser(command.name)
        cmd_parser.set_defaults(func=command.run)
        for arg in command.opts.keys():
            cmd_parser.add_argument(arg, **command.opts[arg])

    if len(sys.argv) == 1:
        parser.print_help()
        raise SystemExit(0)

    args, unknown = parser.parse_known_args()
    func = args.func
    func(sys.argv[2:])


raise SystemExit(main())
