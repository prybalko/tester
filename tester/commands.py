""" Implementation of the commands for CLI scripts. """

import contextlib
import os

import pytest

from tester.lib import is_pid_running
from tester.models import DB, Test


class Command:

    """Command class for the CLI script"""

    def __init__(self, name, opts):
        """
        Command objects are loaded at run-time and injected into command parser.
        *name* denotes the name of the sub-command parser.
        *opts* must be an argparse-compatible dictionary of command options.
        """
        self.name = name
        self.opts = opts

    def run(self, *args, **kwargs):
        """Run the command"""
        raise NotImplementedError


class RunCommand(Command):

    """Run tests."""

    def __init__(self, name='run', opts=None):
        if not opts:
            opts = {'tests': {'type': str,
                              'nargs': '*',
                              'help': 'Run tests in the foreground'},
                    "--tx": {'dest': 'tx',
                             'action': 'append',
                             'default': [],
                             'help': (
                                 "add a test execution environment. some examples: "
                                 "--tx popen//python=python2.5 --tx socket=192.168.1.102:8888 "
                                 "--tx ssh=user@codespeak.net//chdir=testcache"
                             )}
                    }
        super(RunCommand, self).__init__(name, opts)

    def run(self, args):
        with DB.connection_context():
            DB.create_tables([Test])
            return pytest.main(args)


class StartCommand(RunCommand):

    """Start tests in the background."""

    def __init__(self):
        super(StartCommand, self).__init__('start')

    def run(self, args):
        pid = os.fork()
        if pid > 0:
            # Exit parent process
            raise SystemExit(0)

        with open(os.devnull, 'w') as devnull:
            with contextlib.redirect_stdout(devnull):
                super().run(args)


class StatusCommand(Command):

    """Get status of tests."""

    def __init__(self):
        opts = {}
        super(StatusCommand, self).__init__('status', opts)

    def run(self, args):
        columns = ('id', 'pid', 'test', 'status')
        row_format = " {:<10}{:<10}{:<50}{:<15}"
        print(row_format.format(*columns))

        for test in Test.select(*[getattr(Test, field) for field in columns]):
            if test.status in ('pending', 'running') and not is_pid_running(test.pid):
                test.status = 'interrupted'
                test.save()
            print(row_format.format(*[getattr(test, field) for field in columns]))
