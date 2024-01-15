#!/usr/bin/python3
"""
Testing Helpers
"""

from io import StringIO
import sys
import unittest


class Helpers(unittest.TestCase):
    """
    class containing all helper fns
    """

    def stdout(self, function, expected_str):
        """
        Tests print result
        """
        self.maxDiff = None
        captured_output = StringIO()
        sys.stdout = captured_output
        function()
        printed_output = captured_output.getvalue()
        self.assertEqual(printed_output, expected_str)
