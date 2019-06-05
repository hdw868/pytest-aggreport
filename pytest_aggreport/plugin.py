import os
import re
import statistics
from collections import OrderedDict
from datetime import datetime

import pkg_resources
import pytest
from beautifultable import BeautifulTable
from py.xml import html


class AggregateResult(object):
    COLUMN_HEADERS = ['TestCase Name', 'Passed', 'Failed', 'Skipped', 'Pass Rate',
                      'AVG (s)', 'MAX (s)', 'MIN (s)', 'STDDEV (s)', ]
    COLUMN_HEADER_CLASSES = ['name', 'passed', 'failed', 'skipped', 'rate',
                             'avg', 'max', 'min', 'stddev', ]
    COLUMN_CLASSES = ['col-name', 'col-passed', 'col-failed', 'col-skipped', 'col-rate',
                      'col-avg', 'col-max', 'col-min', 'col-stddev']

    def __init__(self, name):
        self.name = name
        self.count_passed = 0
        self.count_failed = 0
        self.count_skipped = 0
        self.durations = []

    @property
    def mean(self):
        return statistics.mean(self.durations)

    @property
    def max(self):
        return max(self.durations)

    @property
    def min(self):
        return min(self.durations)

    @property
    def stddev(self):
        return statistics.stdev(self.durations)

    @property
    def pass_rate(self):
        result = 0
        try:
            result = self.count_passed / (self.count_failed + self.count_passed)
        except ZeroDivisionError:
            pass
        return result

    @property
    def formatted_statistics(self):
        return [
            self.name,
            self.count_passed,
            self.count_failed,
            self.count_skipped,
            "{0:.2%}".format(self.pass_rate),
            "{:.2f}".format(self.mean),
            "{:.2f}".format(self.max),
            "{:.2f}".format(self.min),
            "{:.2f}".format(self.stddev),
        ]

    @property
    def html_table_row(self):
        return html.tr([html.td(v, class_=class_) for v, class_ in zip(self.formatted_statistics, self.COLUMN_CLASSES)])


class AggregateReport(object):

    def __init__(self, config):
        self.results = OrderedDict()
        self.calculated = False
        self.start_time_utc = None
        self.end_time_utc = None
        # add custom css when pytest-html is available
        if config.pluginmanager.hasplugin("html"):
            css_path = pkg_resources.resource_filename(__name__, os.path.join('resources', 'aggreport.css'))
            if hasattr(config.option, "css"):
                config.option.css.append(css_path)
            else:
                config.option.css = [css_path]

    def html_summary_table(self):
        tbody = [
            html.tr([html.th(header, class_=header_class)
                     for header, header_class in
                     zip(AggregateResult.COLUMN_HEADERS, AggregateResult.COLUMN_HEADER_CLASSES)],
                    id='aggregate-report-header'), ]
        for result in self.results.values():
            tbody.append(result.html_table_row)
        html_report = html.table(html.tbody(tbody), id='aggregate-report-table')
        return html_report

    def html_summary_text(self):
        text = [html.p(
            'Test started at {} UTC and ended at {} UTC, following is the summary report: '.format(
                self.start_time_utc, self.end_time_utc)),
        ]
        return text

    def toterminal(self):
        tb = BeautifulTable()
        tb.column_headers = AggregateResult.COLUMN_HEADERS
        for result in self.results.values():
            tb.append_row(result.formatted_statistics)
        return tb

    @staticmethod
    def parse_nodeid(nodeid):
        """Returns the class and method name and id from the current test"""
        names = nodeid.split("::")
        names[0] = names[0].replace("/", ".")
        names = [x.replace(".py", "") for x in names if x != "()"]
        class_names = names[:-1]
        class_name = ".".join(class_names)
        name = names[-1]
        pattern = re.compile(r'(.+)\[(.+)\]')
        name = pattern.match(name).group(1) if pattern.match(name) else name
        index = pattern.match(name).group(2) if pattern.match(name) else '1-1'
        return class_name, name, index

    @pytest.mark.optionalhook
    def pytest_html_results_summary(self, prefix, summary, postfix):
        prefix.extend([self.html_summary_text()])
        prefix.extend([self.html_summary_table()])

    @pytest.mark.hookwrapper(trylast=True)
    def pytest_runtest_makereport(self, item, call):
        outcome = yield
        report = outcome.get_result()
        test_name = self.parse_nodeid(report.nodeid)[1]
        # Get result object
        if self.results.get(test_name) is None:
            self.results[test_name] = AggregateResult(test_name)
        result = self.results.get(test_name)
        # skip will not has attr wasxfail
        if report.skipped and not hasattr(report, "wasxfail"):
            result.count_skipped += 1
            result.durations.append(0)
        if report.when == 'call':
            report.call_start = call.start
            report.call_stop = call.stop
            result.durations.append(report.duration)
            if report.passed:
                result.count_passed += 1
            elif report.failed:
                result.count_failed += 1
            # xfail will get skipped outcome when test fail
            elif report.skipped:
                result.count_failed += 1

    def pytest_terminal_summary(self, terminalreporter):
        terminalreporter.write_sep('-', 'aggregate summary report')
        terminalreporter.line(self.toterminal())

    def pytest_sessionstart(self, session):
        self.start_time_utc = datetime.utcnow().replace(microsecond=0)

    def pytest_sessionfinish(self, session):
        self.end_time_utc = datetime.utcnow().replace(microsecond=0)


@pytest.hookimpl(trylast=True)
def pytest_configure(config):
    if config.getoption('count') > 1:
        config._aggreport = AggregateReport(config)
        config.pluginmanager.register(config._aggreport)


def pytest_unconfigure(config):
    aggreport = getattr(config, '_aggreport', None)
    if aggreport:
        del config._aggreport
        config.pluginmanager.unregister(aggreport)
