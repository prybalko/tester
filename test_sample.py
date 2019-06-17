import time

import pytest


def f():
    raise SystemExit(1)


def test_mytest():
    time.sleep(1)
    raise Exception()
    with pytest.raises(SystemExit):
        f()


class TestClass:
    def test_one(self):
        time.sleep(1)
        x = "this"
        assert 'h' in x
