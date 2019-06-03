# -*- coding: utf-8 -*-


def test_toterminal(testdir):
    """Make sure that pytest accepts our fixture."""

    # create a temporary pytest test module
    testdir.makepyfile("""
        import pytest
        def test_pass(): pass
        @pytest.mark.skip()
        def test_skip(): pass
        def test_fail(): assert False
        @pytest.mark.xfail()
        def test_xpass(): pass
        @pytest.mark.xfail()
        def test_xfail(): assert False
    """)

    # run pytest with the following cmd args
    result = testdir.runpytest(
        '--count=10',
        '-v'
    )

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '--aggregate summary report--',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0
