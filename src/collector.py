from _pytest import nodes
from _pytest.python import PyCollector

from src.items import BashItem


class BashCollector(nodes.File, PyCollector):
    """ Collector for bash test files. """

    def collect(self):
        item = BashItem(name=self.name, nodeid=self.nodeid, config=self.config, session=self.session)
        item.fspath = self.fspath
        yield item
