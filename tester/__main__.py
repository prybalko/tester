import argparse
import sys
import datetime
import pytest

from tester.helpers import Command
from tester.models import db, Test


class StartCommand(Command):

    """Start running tests."""

    def __init__(self):
        opts = {'tests': {'type': str,
                          'nargs': '*'},
                }
        super(StartCommand, self).__init__('start', opts)

    def run(self, tests=None):
        db.connect()
        db.create_tables([Test])

        status_code = pytest.main(args=tests)

        db.close()
        return status_code


class StatusCommand(Command):

    """Get status of running tests."""

    def __init__(self):
        opts = {}
        super(StatusCommand, self).__init__('status', opts)

    def run(self):
        print("status")


def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(title="Tester commands")

    commands = [StartCommand(),
                StatusCommand(),
                ]

    for command in commands:
        cmd_parser = subparsers.add_parser(command.name)
        cmd_parser.set_defaults(func=command.run)

        for arg in command.opts.keys():
            cmd_parser.add_argument(arg, **command.opts[arg])

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()
    func = args.func
    del args.func
    func(**vars(args))


raise SystemExit(main())
