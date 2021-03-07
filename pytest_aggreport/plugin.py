import os
import statistics
from collections import OrderedDict, Counter
from datetime import datetime

import beautifultable
import pkg_resources
import pytest
from py.xml import html

COLUMN_HEADERS = ['TestCase Name', 'Passed', 'Failed', 'Skipped', 'Pass Rate',
                  'AVG (s)', 'MAX (s)', 'MIN (s)', 'STDDEV (s)', ]
COLUMN_HEADER_CLASSES = ['name', 'passed', 'failed', 'skipped', 'rate',
                         'avg', 'max', 'min', 'stddev', ]
COLUMN_CLASSES = ['col-name', 'col-passed', 'col-failed', 'col-skipped',
                  'col-rate',
                  'col-avg', 'col-max', 'col-min', 'col-stddev']


def pytest_addhooks(pluginmanager):
    from pytest_aggreport import hooks
    pluginmanager.add_hookspecs(hooks)


class CaseReport(object):

    def __init__(self, name, config):
        self.name = name
        self.config = config
        self.count_passed = 0
        self.count_failed = 0
        self.count_skipped = 0
        self.durations = []

    @property
    def mean(self):
        if len(self.durations) < 1:
            return 0
        return statistics.mean(self.durations)

    @property
    def max(self):
        if len(self.durations) < 1:
            return 0
        return max(self.durations)

    @property
    def min(self):
        if len(self.durations) < 1:
            return 0
        return min(self.durations)

    @property
    def stddev(self):
        if len(self.durations) < 2:
            return 0
        return statistics.stdev(self.durations)

    @property
    def pass_ratio(self):
        result = 0
        try:
            result = self.count_passed / (
                    self.count_failed + self.count_passed)
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
            "{0:.2%}".format(self.pass_ratio),
            "{:.2f}".format(self.mean),
            "{:.2f}".format(self.max),
            "{:.2f}".format(self.min),
            "{:.2f}".format(self.stddev),
        ]

    @property
    def terminal_table_row(self):
        cells = self.formatted_statistics
        self.config.hook.pytest_aggreport_terminal_table_row(result=self,
                                                             cells=cells)
        return cells

    @property
    def html_table_row(self):
        cells = html.tr(
            [html.td(v, class_=class_) for v, class_ in
             zip(self.formatted_statistics, COLUMN_CLASSES)])
        self.config.hook.pytest_aggreport_html_table_row(result=self,
                                                         cells=cells)
        return cells


class SessionReport(object):

    def __init__(self, config):
        self.case_reports = OrderedDict()
        self.start_time_utc = None
        self.end_time_utc = None
        self.config = config
        # add custom css when pytest-html is available
        if config.pluginmanager.hasplugin("html"):
            css_path = pkg_resources.resource_filename(__name__, os.path.join(
                'resources', 'aggreport.css'))
            if hasattr(config.option, "css"):
                config.option.css.append(css_path)
            else:
                config.option.css = [css_path]

    @property
    def html_summary_table(self):
        cells = [html.th(header, class_=header_class)
                 for header, header_class in
                 zip(COLUMN_HEADERS, COLUMN_HEADER_CLASSES)]
        self.config.hook.pytest_aggreport_html_table_header(
            cells=cells)
        tbody = [
            html.tr(cells,
                    id='aggregate-report-header'), ]
        for case_report in self.case_reports.values():
            tbody.append(case_report.html_table_row)
        html_report = html.table(html.tbody(tbody),
                                 id='aggregate-report-table')
        return html_report

    @property
    def html_summary_text(self):
        text = [html.p(
            'Test started at {} UTC and ended at {} UTC, '
            'following is the summary report: '.format(
                self.start_time_utc, self.end_time_utc)), ]
        return text

    @property
    def terminal_table(self):
        tb = beautifultable.BeautifulTable()
        cells = list(COLUMN_HEADERS)
        self.config.hook.pytest_aggreport_terminal_table_header(
            cells=cells)
        tb.columns.header = cells
        for result in self.case_reports.values():
            tb.rows.append(result.terminal_table_row)
        return tb

    @staticmethod
    def parse_nodeid(nodeid):
        """Returns the class and method name and id from the current test"""
        path, possible_open_bracket, param = nodeid.partition("[")
        names = path.split("::")
        try:
            names.remove("()")
        except ValueError:
            pass
        # convert file path to dotted path and remove .py
        names[0] = names[0].replace('/', ".")
        names = [x.replace(".py", "") for x in names if x != "()"]
        if param:
            param = param.rstrip(']')
        return names, param

    @pytest.hookimpl(optionalhook=True)
    def pytest_html_results_summary(self, prefix, summary, postfix):
        prefix.extend([self.html_summary_text])
        prefix.extend([self.html_summary_table])

    def pytest_runtest_logreport(self, report):
        names, param = self.parse_nodeid(report.nodeid)
        func_name = '.'.join(names)
        # Get case report object
        if self.case_reports.get(func_name) is None:
            self.case_reports[func_name] = CaseReport(func_name, self.config)
        case_report = self.case_reports.get(func_name)
        # skip will not has attr wasxfail
        if report.skipped and not hasattr(report, "wasxfail"):
            case_report.count_skipped += 1
            case_report.durations.append(0)
        if report.when == 'call':
            case_report.durations.append(report.duration)
            if report.passed:
                case_report.count_passed += 1
            elif report.failed:
                case_report.count_failed += 1
            # xfail will get skipped outcome when test fail
            elif report.skipped and hasattr(report, "wasxfail"):
                case_report.count_failed += 1

    def pytest_terminal_summary(self, terminalreporter):
        terminalreporter.write_sep('-', 'aggregate summary report')
        terminalreporter.line(str(self.terminal_table))

    def pytest_sessionstart(self, session):
        self.start_time_utc = datetime.utcnow().replace(microsecond=0)

    def pytest_sessionfinish(self, session):
        self.end_time_utc = datetime.utcnow().replace(microsecond=0)

    def _make_outcome_summary(self):
        outcome_summary = Counter(
            [result.value().outcome for result in
             self.case_reports])
        outcome_summary['total'] = sum(outcome_summary.values())
        overall_passed = (
                outcome_summary.get('passed', 0)
                + outcome_summary.get('xpassed', 0))
        outcome_summary['pass_ratio'] = overall_passed / outcome_summary[
            'total']
        return outcome_summary


@pytest.hookimpl(trylast=True)
def pytest_configure(config):
    if config.getoption('count') > 1 and not hasattr(config, 'slaveinput'):
        config._aggreport = SessionReport(config)
        config.pluginmanager.register(config._aggreport)


def pytest_unconfigure(config):
    aggreport = getattr(config, '_aggreport', None)
    if aggreport:
        del config._aggreport
        config.pluginmanager.unregister(aggreport)
