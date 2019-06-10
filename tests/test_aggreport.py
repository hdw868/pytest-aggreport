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
"""


class TestTerminal(object):
    def test_terminal_report(self, testdir):
        """Make sure that the result will generate terminal report"""
        # create a temporary pytest test module
        testdir.makepyfile(EXAMPLE_CODE)
        # run pytest with the following cmd args
        result = testdir.runpytest(
            '--count=100',
            '--tb=no',
        )
        # test terminal result
        result.stdout.fnmatch_lines([
            '*- aggregate summary report -*',
            '| TestCase Na | Pass | Fail | Skipp |'
            ' Pass R | AVG ( | MAX ( | MIN ( | STDDEV  |',
            '|  test_pass  | 100  |  0   |   0   |'
            ' 100.00 | 0.01  | *  | 0.01  |   0.0   |',
            '|  test_skip  |  0   |  0   |  100  |'
            ' 0.00%  |  0.0  |  0.0  |  0.0  |   0.0   |',
            '|  test_fail  |  0   | 100  |   0   | '
            '0.00%  | 0.01  | *  | 0.01  |   0.0   |',
            '| test_xpass  | 100  |  0   |   0   | '
            '100.00 | 0.01  | *  | 0.01  |   0.0   |',
            '| test_xfail  |  0   | 100  |   0   |'
            ' 0.00%  | 0.01  | *  | 0.01  |   0.0   |'
        ])
        # test run result outcomes
        result.assert_outcomes(passed=100, failed=100, xfailed=100,
                               xpassed=100, skipped=100)

    def test_custom_content_in_terminal(self, testdir):
        """Make sure that the result will generate terminal report"""
        # create a temporary pytest contest.py file
        testdir.makeconftest("""
            import pytest
            import statistics

            from py.xml import html

            @pytest.hookimpl(optionalhook=True)
            def pytest_aggreport_terminal_table_header(cells):
                cells.append('Extra')


            @pytest.hookimpl(optionalhook=True)
            def pytest_aggreport_terminal_table_row(result, cells):
                cells.append(statistics.median(result.durations))
        """)
        # create a temporary pytest test module
        testdir.makepyfile(EXAMPLE_CODE)

        # run pytest with the following cmd args
        result = testdir.runpytest(
            '--count=100',
            '--tb=no',
            '--html=report.html',
        )
        # test terminal result
        result.stdout.fnmatch_lines([
            '*- aggregate summary report -*',
            '| TestCase N | Pas | Fail | Skipp |'
            ' Pass R | AVG  | MAX  | MIN  | STDDEV | Ext |',
            '| test_pass  | 100 |  0   |   0   |'
            ' 100.00 | 0.01 | * | 0.01 |  0.0   | 0.0 |',
            '| test_skip  |  0  |  0   |  100  | '
            '0.00%  | 0.0  | *  | 0.0  |  0.0   | 0.0 |',
            '| test_fail  |  0  | 100  |   0   | '
            '0.00%  | 0.01 | * | 0.01 |  0.0   | 0.0 |',
            '| test_xpass | 100 |  0   |   0   | '
            '100.00 | 0.01 | * | 0.01 |  0.0   | 0.0 |',
            '| test_xfail |  0  | 100  |   0   | '
            '0.00%  | 0.01 | * | 0.01 |  0.0   | 0.0 |'
        ])
        # test run result outcomes
        result.assert_outcomes(passed=100, failed=100, xfailed=100,
                               xpassed=100, skipped=100)


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
                               xpassed=100, skipped=100)
        assert_results_by_col(html, 'col-name',
                              ['test_pass', 'test_skip', 'test_fail',
                               'test_xpass', 'test_xfail'])
        assert_results_by_col(html, 'col-passed',
                              ['100', '0', '0', '100', '0'])
        assert_results_by_col(html, 'col-failed',
                              ['0', '0', '100', '0', '100'])
        assert_results_by_col(html, 'col-skipped', ['0', '100', '0', '0', '0'])
        assert_results_by_col(html, 'col-rate',
                              ['100.00%', '0.00%', '0.00%', '100.00%',
                               '0.00%'])
        assert_results_by_col(html, 'col-min',
                              ['0.01', '0.00', '0.01', '0.01', '0.01'])

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
                cells.append(
                    html.td("{:.2f}".format(
                        statistics.median(result.durations)),
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
                               xpassed=100, skipped=100)
        assert_results_by_col(html, 'col-name',
                              ['test_pass', 'test_skip', 'test_fail',
                               'test_xpass', 'test_xfail'])
        assert_results_by_col(html, 'col-extra',
                              ['0.01', '0.00', '0.01', '0.01', '0.01'])
