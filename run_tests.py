"""Test runner module."""
import unittest
import coverage

def run_tests_with_coverage():
    """Run tests with coverage reporting."""
    # Start coverage monitoring
    cov = coverage.Coverage(
        branch=True,
        source=['app'],
        omit=[
            '*/tests/*',
            '*/migrations/*',
            '*/venv/*',
            '*/__init__.py'
        ]
    )
    cov.start()

    # Run tests
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Stop coverage monitoring and generate report
    cov.stop()
    cov.save()

    # Print coverage report
    print('\nCoverage Summary:')
    cov.report()

    # Generate HTML report
    cov.html_report(directory='coverage_report')
    print('\nDetailed HTML coverage report generated in coverage_report/index.html')

    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests_with_coverage()
    exit(0 if success else 1)
