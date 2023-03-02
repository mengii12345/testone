import unittest

from test_unittest.Base.PublicFunction import render_directory
from test_unittest.TestCase import Login_test

suite = unittest.TestSuite()
TestCases = unittest.TestLoader().loadTestsFromModule(Login_test)
suite.addTest(TestCases)
runner = unittest.TextTestRunner()
runner.run(suite)

render_directory()
