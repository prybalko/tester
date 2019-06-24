import os
import stat
from functools import partial

import pytest

pytest_plugins = ["pytester"]


def makebashfile(self, *args, **kwargs):
    """Shortcut for .makefile() with a .bash extension."""
    path = self._makefile(".sh", args, kwargs)
    st = os.stat(path)
    os.chmod(path, st.st_mode | stat.S_IEXEC)
    return path


@pytest.fixture
def ourtestdir(testdir):
    testdir.makebashfile = partial(makebashfile, testdir)
    yield testdir


def test_bash_test(ourtestdir):
    ourtestdir.makebashfile(
        test_one="""
                #!/bin/sh
                exit 0
                """
    )
    out = ourtestdir.run('tester', 'run')
    out.assert_outcomes(passed=1)


def test_failed_bash_test(ourtestdir):
    ourtestdir.makebashfile(
        test_fail="""
                #!/bin/sh
                exit 1
                """
    )
    out = ourtestdir.run('tester', 'run')
    out.assert_outcomes(failed=1)
