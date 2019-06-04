# -*- coding: utf-8 -*-

pytest_plugins = "pytester"


def test_terminal_report(testdir):
    """Make sure that the result will generate terminal report"""
    # create a temporary pytest test module
    testdir.makepyfile("""
        import time
        import pytest
        def test_pass(): 
            time.sleep(0.1)
            pass
        
        @pytest.mark.skip()
        def test_skip(): 
            time.sleep(0.1)
            pass
            
        def test_fail(): 
            time.sleep(0.15)
            assert False
        
        @pytest.mark.xfail()
        def test_xpass():
            time.sleep(0.1)
            pass
        
        @pytest.mark.xfail()
        def test_xfail(): 
            time.sleep(0.1)
            assert False
    """)

    # run pytest with the following cmd args
    result = testdir.runpytest(
        '--count=5',
    )
    # test terminal result
    result.stdout.fnmatch_lines_random('*- aggregate summary report -*')
    result.stdout.fnmatch_lines_random(
        '|  test_pass  |  5   |  0   |   0   | 100.00 |  0.1  |  0.1  |  0.1  |   0.0   |')
    result.stdout.fnmatch_lines_random(
        '|  test_skip  |  0   |  0   |   5   | 0.00%  |  0.0  |  0.0  |  0.0  |   0.0   |')
    result.stdout.fnmatch_lines_random(
        '|  test_fail  |  0   |  5   |   0   | 0.00%  | 0.15  | 0.15  | 0.15  |   0.0   |')
    result.stdout.fnmatch_lines_random(
        '| test_xpass  |  5   |  0   |   0   | 100.00 |  0.1  |  0.1  |  0.1  |   0.0   |')
    result.stdout.fnmatch_lines_random(
        '| test_xfail  |  0   |  5   |   0   | 0.00%  |  0.1  |  0.1  |  0.1  |   0.0   |')
    # test run result outcomes
    result.assert_outcomes(passed=5, failed=5, xfailed=5, xpassed=5, skipped=5)
