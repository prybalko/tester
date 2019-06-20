import datetime

import pytest

from src.collector import BashCollector
from src.tester import Test


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # we only look at actual test calls, not setup/teardown
    if rep.when == "call":
        test = Test.get(id=item.test_id)
        test.status = rep.outcome
        test.finished_at = datetime.datetime.now()
        if rep.failed:
            test.logs = rep.longrepr.reprcrash.message
        test.save()


def pytest_runtest_setup(item):
    test = Test.get(id=item.test_id)
    test.started_at = datetime.datetime.now()
    test.save()


def pytest_collect_file(path, parent):
    if path.ext == ".sh" and path.purebasename.startswith('test_'):
        return BashCollector(path, parent)


def pytest_collection_finish(session):
    for item in session.items:
        test = Test.create(test=item.nodeid)
        setattr(item, "test_id", test.id)
