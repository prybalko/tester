import traceback
from subprocess import PIPE, run

from _pytest.nodes import Item

from src.exceptions import BashTestFailure


class BashItem(Item):

    def runtest(self):
        result = run(self.fspath.strpath, stderr=PIPE)
        if not result.returncode == 0:
            raise BashTestFailure(result.stderr)
