import six
import pytest
from twisted.python import log

collect_ignore = [
    "scrapy/conf.py",
    "scrapy/stats.py",
    "scrapy/project.py",
    "scrapy/contrib_exp/__init__.py",
    "scrapy/contrib_exp/iterators.py",
    "scrapy/contrib_exp/downloadermiddleware/__init__.py",
    "scrapy/contrib_exp/downloadermiddleware/decompression.py",
]

if six.PY3:
    for line in open('tests/py3-ignores.txt'):
        file_path = line.strip()
        if len(file_path) > 0 and file_path[0] != '#':
            collect_ignore.append(file_path)


class LogObservers:
    """Class for keeping track of log observers across test modules"""

    def __init__(self):
        self.observers = []

    def add(self, logfile='test.log'):
        fileobj = open(logfile, 'wb')
        observer = log.FileLogObserver(fileobj)
        log.startLoggingWithObserver(observer.emit, 0)
        self.observers.append((fileobj, observer))

    def remove(self):
        fileobj, observer = self.observers.pop()
        log.removeObserver(observer.emit)
        fileobj.close()


@pytest.fixture(scope='module')
def log_observers():
    return LogObservers()


@pytest.fixture()
def setlog(request, log_observers):
    """Attach test.log file observer to twisted log, for trial compatibility"""
    log_observers.add()
    request.addfinalizer(log_observers.remove)


@pytest.fixture()
def chdir(tmpdir):
    """Change to pytest-provided temporary directory"""
    tmpdir.chdir()
