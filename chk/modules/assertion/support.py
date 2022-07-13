"""
Assertion related services
"""
from io import StringIO
from unittest import TestCase, TestSuite, TextTestRunner


class AssertionCase(TestCase):
    def __init__(self, name: str, arg1, arg2):
        super(AssertionCase, self).__init__(name)
        self.type = type
        self.arg1 = arg1
        self.arg2 = arg2

    def case_AssertEqual(self):
        self.assertEqual(self.arg1, self.arg2)

    def case_AssertDictEqual(self):
        self.assertDictEqual(self.arg1, self.arg2)


class AssertionHandler:
    """
    AssertionHandler
    """

    @staticmethod
    def asserts_test_run(assertions: list):
        """
        Process given assertions and run test based on those
        :param assertions: list of passed assertions
        :return:
        """
        suite = TestSuite()

        for each_assertion in assertions:
            suite.addTest(AssertionCase(f"case_{each_assertion.type}", each_assertion.actual, each_assertion.expected))

        run_result = TextTestRunner(stream=StringIO(), verbosity=0).run(suite)

