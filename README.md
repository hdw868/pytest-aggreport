# pytest-aggreport

![PyPI version](https://camo.githubusercontent.com/71bf14eb443946de8ccc2fc8efd5a787845ffba9/68747470733a2f2f696d672e736869656c64732e696f2f707970692f762f7079746573742d6167677265706f72742e737667) ![Python versions](https://camo.githubusercontent.com/3997b7d5a231a8ad2161e25b673bf4ad502f7dc4/68747470733a2f2f696d672e736869656c64732e696f2f707970692f707976657273696f6e732f7079746573742d6167677265706f72742e737667) ![See Build Status on Travis CI](https://camo.githubusercontent.com/b2142eb9443757b035943a81c5b4f6ef7e3275c4/68747470733a2f2f7472617669732d63692e6f72672f6864773836382f7079746573742d6167677265706f72742e7376673f6272616e63683d6d6173746572)

This [pytest](https://github.com/pytest-dev/pytest) plugin was generated with [Cookiecutter](https://github.com/audreyr/cookiecutter) along with [@hackebrot](https://github.com/hackebrot)'s [cookiecutter-pytest-plugin](https://github.com/pytest-dev/cookiecutter-pytest-plugin) template.

## Features

- Generate aggregated test result group by test case name with details;
- Embed test result into html report if pytest-html is available;



## Requirements

- python >= 3.6
- pytest >= 4.3.1
- beautifultable >= 0.7.0
- pytest-repeat >= 0.8.0



## Installation

You can install "pytest-aggreport" via [pip](https://pypi.org/project/pip/) from [PyPI](https://pypi.org/project):

```bash
$ pip install pytest-aggreport
```



## Usage

Pytest will automatically find the plugin and use it when you run pytest with `--count` argument (enable [pytest-repeat](https://github.com/pytest-dev/pytest-repeat) plugin). When test is done, you will see a summary report in the terminal:

```bash
$ pytest --count=5
...
------------------------- aggregate summary report -----------------
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
```

If [pytest-html](https://github.com/pytest-dev/pytest-html) is enabled(run with `--html` argument), then a summary report will also be embedded in the html report:

![html_report](docs/html_report.png)

To disable the plugin, you can use the `-p` argument, for example:

```bash
$ pytest -p no:aggreport
```



## Contributing

Contributions are very welcome. Tests can be run with [tox](https://tox.readthedocs.io/en/latest/), please ensure the coverage at least stays the same before you submit a pull request.



## License

Distributed under the terms of the [MIT](http://opensource.org/licenses/MIT) license, "pytest-aggreport" is free and open source software



## Issues

If you encounter any problems, please [file an issue](https://github.com/hdw868/pytest-aggreport/issues) along with a detailed description.