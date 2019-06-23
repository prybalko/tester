import contextlib
import os

import pytest

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

    """Start process in the background."""

    def __init__(self):
        opts = {'tests': {'type': str,
                          'nargs': '*'}}
        super(RunCommand, self).__init__('run', opts)

    def run(self, tests=None):
        with DB.connection_context():
            DB.create_tables([Test])
            return pytest.main(args=tests)


class StartCommand(RunCommand):

    """Start running tests."""

    def __init__(self):
        opts = {'tests': {'type': str,
                          'nargs': '*'}}
        super(RunCommand, self).__init__('start', opts)

    def run(self, tests=None):
        pid = os.fork()
        if pid > 0:
            # Exit parent process
            raise SystemExit(0)

        with open(os.devnull, 'w') as devnull:
            with contextlib.redirect_stdout(devnull):
                super().run(tests)


class StatusCommand(Command):

    """Get status of running tests."""

    def __init__(self):
        opts = {}
        super(StatusCommand, self).__init__('status', opts)

    def run(self):
        columns = ('id', 'pid', 'test', 'status')
        row_format = " {:<10}{:<10}{:<50}{:<15}"
        print(row_format.format(*columns))

        for test in Test.select(*[getattr(Test, field) for field in columns]):
            if test.status in ('pending', 'running') and not self._is_pid_alive(test.pid):
                test.status = 'interrupted'
                test.save()
            print(row_format.format(*[getattr(test, field) for field in columns]))

    def _is_pid_alive(self, pid):
        """ Check for the existence of a unix pid. """
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        return True
