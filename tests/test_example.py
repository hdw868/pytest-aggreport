import pytest
import time


def test_pass():
    time.sleep(0.1)
    pass


@pytest.mark.skip()
def test_skip(): pass


def test_fail():
    time.sleep(0.15)
    assert False


@pytest.mark.xfail()
def test_xpass(): pass


@pytest.mark.xfail()
def test_xfail(): assert False
