import unittest
import coverage


def run_tests_with_coverage():
    cov = coverage.Coverage()
    cov.start()

    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover("../test", pattern="*Test.py")
    unittest.TextTestRunner(verbosity=2).run(test_suite)

    cov.stop()
    cov.report()


if __name__ == "__main__":
    run_tests_with_coverage()

