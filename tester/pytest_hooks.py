import datetime

import pytest

from tester.collectors import BashCollector
from tester.models import Test


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """ execute all other hooks to obtain the report object

    return a :py:class:`_pytest.runner.TestReport` object
    for the given :py:class:`pytest.Item <_pytest.main.Item>` and
    :py:class:`_pytest.runner.CallInfo`. """
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call":
        test = Test.get(id=item.test_id)
        test.status = rep.outcome
        test.finished_at = datetime.datetime.now()
        if rep.failed:
            test.logs = rep.longrepr.reprcrash.message
        test.save()


def pytest_runtest_setup(item):
    """ called before executing each test item. """
    test = Test.get(id=item.test_id)
    test.started_at = datetime.datetime.now()
    test.status = 'running'
    test.save()


def pytest_collect_file(path, parent):
    """ return collection Node or None for the given path. Any new node
    needs to have the specified ``parent`` as a parent.

    :param path: a :py:class:`py.path.local` - the path to collect
    """
    if path.ext == ".sh" and path.purebasename.startswith('test_'):
        return BashCollector(path, parent)


def pytest_collection_finish(session):
    """ called after collection has been performed and modified.

    :param _pytest.main.Session session: the pytest session object
    """
    for item in session.items:
        test = Test.create(test=item.nodeid)
        setattr(item, "test_id", test.id)
