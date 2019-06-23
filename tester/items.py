""" A test invocation items. """

from subprocess import PIPE, run

from _pytest.nodes import Item


class BashItem(Item):
    """ A Bash script Item is responsible for executing a Bash test file. """

    def runtest(self):
        """ Execute the underlying test file. """
        result = run(self.fspath.strpath, stderr=PIPE)
        if not result.returncode == 0:
            raise AssertionError(result.stderr)
