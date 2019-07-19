# -*- coding: utf-8 -*-
import re

pytest_plugins = "pytester"
EXAMPLE_CODE = """
import time
import pytest
def test_pass():
    time.sleep(0.01)
    pass

@pytest.mark.skip()
def test_skip():
    time.sleep(0.01)
    pass

def test_fail():
    time.sleep(0.01)
    assert False

@pytest.mark.xfail()
def test_xpass():
    time.sleep(0.01)
    pass

@pytest.mark.xfail()
def test_xfail():
    time.sleep(0.01)
    assert False

def test_inline_skip():
    time.sleep(0.01)
    pytest.skip()
    assert False

@pytest.fixture()
def flaky_thing():
    raise RuntimeError('Ops, something wrong happened!')

def test_error(flaky_thing):
    pass

"""


def read_html(path):
    with open(str(path)) as f:
        return f.read()


def assert_results_by_col(html, col, values):
    # Asserts if the table rows of this outcome are correct
    regex_col = ('<td class="{}">(.*)</td>'.format(col))
    for i, item in enumerate(re.findall(regex_col, html)[:len(values)]):
        assert item == values[i]


class TestHTML(object):
    def test_html_report(self, testdir):
        testdir.makepyfile(EXAMPLE_CODE)
        path = testdir.tmpdir.join('report.html')
        result = testdir.runpytest('--html={}'.format(path),
                                   '--count=100',
                                   '--tb=no'
                                   )
        html = read_html(path)

        # test run result outcomes
        result.assert_outcomes(passed=100, failed=100, xfailed=100,
                               xpassed=100, skipped=200, error=100)
        assert_results_by_col(html, 'col-name',
                              ['test_html_report.test_pass',
                               'test_html_report.test_skip',
                               'test_html_report.test_fail',
                               'test_html_report.test_xpass',
                               'test_html_report.test_xfail',
                               'test_html_report.test_inline_skip',
                               'test_html_report.test_error',
                               ])
        assert_results_by_col(html, 'col-passed',
                              ['100', '0', '0', '100', '0', '0', '0'])
        assert_results_by_col(html, 'col-failed',
                              ['0', '0', '100', '0', '100', '0', '0'])
        assert_results_by_col(html, 'col-skipped',
                              ['0', '100', '0', '0', '0', '100', '0'])
        assert_results_by_col(html, 'col-rate',
                              ['100.00%', '0.00%', '0.00%', '100.00%',
                               '0.00%', '0.00%', '0.00%'])
        assert_results_by_col(html, 'col-min',
                              ['0.01', '0.00', '0.01', '0.01', '0.01',
                               '0.00', '0.00'])

    def test_custom_html_report(self, testdir):
        # create a temporary pytest contest.py file
        testdir.makeconftest("""
            import pytest
            import statistics

            from py.xml import html
            @pytest.hookimpl(optionalhook=True)
            def pytest_aggreport_html_table_header(cells):
                cells.append(html.th('Extra'))


            @pytest.hookimpl(optionalhook=True)
            def pytest_aggreport_html_table_row(result, cells):
                median = 0
                if len(result.durations) > 1:
                    median = statistics.median(result.durations)
                cells.append(
                    html.td("{:.2f}".format(median),
                        class_='col-extra'))
        """)
        testdir.makepyfile(EXAMPLE_CODE)
        path = testdir.tmpdir.join('report.html')
        result = testdir.runpytest('--html={}'.format(path),
                                   '--count=100',
                                   '--tb=no'
                                   )
        html = read_html(path)
        # test run result outcomes
        result.assert_outcomes(passed=100, failed=100, xfailed=100,
                               xpassed=100, skipped=200, error=100)
        assert_results_by_col(html, 'col-name',
                              ['test_custom_html_report.test_pass',
                               'test_custom_html_report.test_skip',
                               'test_custom_html_report.test_fail',
                               'test_custom_html_report.test_xpass',
                               'test_custom_html_report.test_xfail',
                               'test_custom_html_report.test_inline_skip',
                               'test_custom_html_report.test_error'])
        assert_results_by_col(html, 'col-extra',
                              ['0.01', '0.00', '0.01', '0.01', '0.01',
                               '0.01', '0.00'])

    def test_xdist_compatibality(self, testdir):
        testdir.makepyfile(EXAMPLE_CODE)
        path = testdir.tmpdir.join('report.html')
        result = testdir.runpytest('--html={}'.format(path),
                                   '--count=100',
                                   '--tb=no',
                                   '-n=5'
                                   )
        html = read_html(path)

        # test run result outcomes
        result.assert_outcomes(passed=100, failed=100, xfailed=100,
                               xpassed=100, skipped=200, error=100)
        assert_results_by_col(html, 'col-name',
                              ['test_xdist_compatibality.test_pass',
                               'test_xdist_compatibality.test_skip',
                               'test_xdist_compatibality.test_fail',
                               'test_xdist_compatibality.test_xpass',
                               'test_xdist_compatibality.test_xfail',
                               'test_xdist_compatibality.test_inline_skip',
                               'test_xdist_compatibality.test_error',
                               ])
        assert_results_by_col(html, 'col-passed',
                              ['100', '0', '0', '100', '0', '0', '0'])
        assert_results_by_col(html, 'col-failed',
                              ['0', '0', '100', '0', '100', '0', '0'])
        assert_results_by_col(html, 'col-skipped',
                              ['0', '100', '0', '0', '0', '100', '0'])
        assert_results_by_col(html, 'col-rate',
                              ['100.00%', '0.00%', '0.00%', '100.00%',
                               '0.00%', '0.00%', '0.00%'])
        assert_results_by_col(html, 'col-min',
                              ['0.01', '0.00', '0.01', '0.01', '0.01',
                               '0.00', '0.00'])
