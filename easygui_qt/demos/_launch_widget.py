from __future__ import print_function
"""This file is meant to be executed as a subprocess from launcher.py"""

import locale
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../"))
func_name = sys.argv[1]

try:
    import easygui_qt
    func = getattr(easygui_qt, func_name)
except:
    try:
        from easygui_qt import easygui_qt
        func = getattr(easygui_qt, func_name)
    except:
        print("could not find function {}".format(func_name))
        sys.exit()

if len(sys.argv) > 2:
    args = tuple([sys.argv[i] for i in range(2,len(sys.argv))])
    result = func(*args)
else:
    result = func()

if sys.version_info < (3,):
    try:
        res = bytearray(result, encoding=locale.getdefaultlocale()[1])
        result = res
    except:
        pass

print(result, end='')

