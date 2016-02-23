"""
Basic test suite, loosely based on unittest from Pyunit.
"""


class TestSuite:
    """
    Simple testing class for creating test suites
    inspired by unittest from Pyunit
    (https://docs.python.org/2/library/unittest.html)
    """
    def __init__(self):
        """
        Creates a test suite object
        """
        self.total_tests = 0
        self.failures = 0
    
    
    def run_test(self, computed, expected, message = ""):
        """
        Compare computed and expected
        If not equal, print message, computed, expected
        """
        self.total_tests += 1
        if computed != expected:
            msg = message + " Computed: " + str(computed)
            msg += " Expected: " + str(expected)
            print msg
            self.failures += 1
    
    def report_results(self):
        """
        Report back summary of successes and failures
        from run_test()
        """
        msg = "Ran " + str(self.total_tests) + " tests. "
        msg += str(self.failures) + " failures."
        print msg