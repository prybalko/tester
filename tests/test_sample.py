import time


def test_mytest():
    time.sleep(20)
    # raise Exception("that's the reason this test failed")


class TestClass:
    def test_one(self):
        # time.sleep(.1)
        x = "this"
        assert 'h' in x
