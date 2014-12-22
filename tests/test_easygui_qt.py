"""
test_easygui_qt
----------------------------------

Tests for `easygui_qt` module.

Meant to be run from parent directory using
python -m unittest discover

Important:

* I use "pyconda" as an alias for my python interpreter used to run these tests.
* These tests pop up various windows. They should run uninterrupted by
  mouse or keyboard activities to prevent problems
"""

import unittest
import subprocess
import threading
import time

import pyautogui


class TypewriteThread(threading.Thread):
    """Sends key strokes to a window/dialog."""
    def __init__(self, msg, interval=0.0):
        super(TypewriteThread, self).__init__()
        self.msg = msg
        self.interval = interval

    def run(self):
        """Start running the test after a brief pause to allow
           the window or dialog to show on the screen
        """
        time.sleep(1.5)
        pyautogui.typewrite(self.msg, self.interval)


class TestTextInput(unittest.TestCase):

    def setUp(self):
        self.args = 'pyconda tests/show_get_string.py'
        self.kwd = {'universal_newlines': True}

    def set_writer(self, arg):
        t = TypewriteThread(arg)
        t.start()

    def test_something(self):
        test_string = "Hi!"
        self.set_writer('{}\n'.format(test_string))  # \n equivalent to "enter"
        self.output = subprocess.check_output(self.args, **self.kwd)
        self.assertEqual(test_string, self.output, "string input test")

    def test_ok(self):
        self.set_writer(['tab', 'enter'])
        self.output = subprocess.check_output(self.args, **self.kwd)
        self.assertEqual('', self.output, "OK button activated")

    def test_cancel(self):
        self.set_writer(['tab', 'tab', 'enter'])
        self.output = subprocess.check_output(self.args, **self.kwd)
        self.assertEqual('None', self.output, "cancel button activated")

    def test_escape(self):
        self.set_writer(['esc'])
        self.output = subprocess.check_output(self.args, **self.kwd)
        self.assertEqual('None', self.output, "escape key")

class TestTextInputWithDefaultArgument(TestTextInput):

    def setUp(self):
        self.args = 'pyconda tests/show_get_string2.py'
        self.kwd = {'universal_newlines': True}

    def test_ok(self):
        self.set_writer(['tab', 'enter'])
        self.output = subprocess.check_output(self.args, **self.kwd)
        self.assertEqual("Hello", self.output, "OK button activated")

if __name__ == '__main__':
    unittest.main()
