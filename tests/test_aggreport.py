# -*- coding: utf-8 -*-


def test_toterminal(testdir):
    """Make sure that the result will generate terminal report"""

    # create a temporary pytest test module
    testdir.makepyfile("""
        import time
        import pytest
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
    """)

    # run pytest with the following cmd args
    result = testdir.runpytest(
        '--count=5',
    )

    # make sure that that we get a '1' exit code for the testsuite
    assert result.ret == 1


# def test_parse_nodeid(testdir):
#     """Make sure that parse_nodeid function works properly."""
#
#     # create a temporary pytest test module
#     testdir.makepyfile("""
#         def test_abc(): pass
#         class TestClassA
#             def test_abc(self): pass
#     """)
#
#     # run pytest with the following cmd args
#     result = testdir.runpytest(
#         '--count=5',
#     )
#
#     # fnmatch_lines does an assertion internally
#     result.stdout.fnmatch_lines([
#         'aggregate summary report',
#     ])
#
#     # make sure that that we get a '0' exit code for the testsuite
#     assert result.ret == 0