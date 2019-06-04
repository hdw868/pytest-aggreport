================
pytest-aggreport
================

.. image:: https://img.shields.io/pypi/v/pytest-aggreport.svg
    :target: https://pypi.org/project/pytest-aggreport
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-aggreport.svg
    :target: https://pypi.org/project/pytest-aggreport
    :alt: Python versions

.. image:: https://travis-ci.org/hdw868/pytest-aggreport.svg?branch=master
    :target: https://travis-ci.org/hdw868/pytest-aggreport
    :alt: See Build Status on Travis CI

.. image:: https://ci.appveyor.com/api/projects/status/github/hdw868/pytest-aggreport?branch=master
    :target: https://ci.appveyor.com/project/hdw868/pytest-aggreport/branch/master
    :alt: See Build Status on AppVeyor

 A report enhance plugin for pytest-repeat that aggregates test result of the same test in terminal and html(if pytest-html is available).

----

This `pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `cookiecutter-pytest-plugin`_ template.


Features
--------

* Generate aggregated test result group by test case name with details;
* Embed test result into html report if pytest-html is available;


Requirements
------------

* pytest >= 4.3.1
* pytest-repeat >= 0.8.0
* beautifultable >= 0.7.0
* python >= 3.6

Installation
------------

You can install "pytest-aggreport" via `pip`_ from `PyPI`_:

::

    $ pip install pytest-aggreport

Usage
-----

Python 3.6-3.7 supported.

Pytest will automatically find the plugin and use it when you run pytest with --count parameter.
When test is done, you will see a summary report in terminal:

::

    $ pytest --count=5
    ...
    ---------------------------------------------- aggregate summary report -----------------------------------------------
    +-------------+------+------+-------+--------+-------+-------+-------+---------+
    | TestCase Na | Pass | Fail | Skipp | Pass R | AVG ( | MAX ( | MIN ( | STDDEV  |
    |     me      |  ed  |  ed  |  ed   |  ate   |  s)   |  s)   |  s)   |   (s)   |
    +-------------+------+------+-------+--------+-------+-------+-------+---------+
    |  test_pass  |  5   |  0   |   0   | 100.00 |  0.1  |  0.1  |  0.1  |   0.0   |
    |             |      |      |       |   %    |       |       |       |         |
    +-------------+------+------+-------+--------+-------+-------+-------+---------+
    |  test_skip  |  0   |  0   |   5   | 0.00%  |  0.0  |  0.0  |  0.0  |   0.0   |
    +-------------+------+------+-------+--------+-------+-------+-------+---------+
    |  test_fail  |  0   |  5   |   0   | 0.00%  | 0.15  | 0.15  | 0.15  |   0.0   |
    +-------------+------+------+-------+--------+-------+-------+-------+---------+
    | test_xpass  |  5   |  0   |   0   | 100.00 |  0.1  |  0.1  |  0.1  |   0.0   |
    |             |      |      |       |   %    |       |       |       |         |
    +-------------+------+------+-------+--------+-------+-------+-------+---------+
    | test_xfail  |  0   |  5   |   0   | 0.00%  |  0.1  |  0.1  |  0.1  |   0.0   |
    +-------------+------+------+-------+--------+-------+-------+-------+---------+
    ...

if pytest-html is used (run with --html parameter), then a summary report will also be generated in html report:

.. image:: html_report
    :target: docs/html_report.PNG

To disable it altogether, you can use the -p argument, for example:

::

   $pytest -p no:aggreport

Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `MIT`_ license, "pytest-aggreport" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/hdw868/pytest-aggreport/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
