import unittest
import HtmlTestRunner

if __name__ == '__main__':
    # Discover all tests in the 'tests/' folder
    suite = unittest.defaultTestLoader.discover('tests')

    runner = HtmlTestRunner.HTMLTestRunner(
        output='html-report',
        report_name='AllTests',
        combine_reports=True,
        add_timestamp=True,
        verbosity=2
    )

    runner.run(suite)

