from __future__ import print_function
"""This file is meant to be executed as a subprocess from launcher.pyw"""

import locale
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../"))
func_name = sys.argv[1]
if len(sys.argv)==3:
    loc_ = sys.argv[2]
else:
    loc_ = None

try:
    import easygui_qt
    func = getattr(easygui_qt, func_name)
    #config = easygui_qt.CONFIG
except:
    try:
        from easygui_qt import easygui_qt
        func = getattr(easygui_qt, func_name)
        #config = easygui_qt.CONFIG
    except:
        print("could not find function {}".format(func_name))
        sys.exit()

#if loc_ is not None:
#    config['locale'] = loc_
result = func()

if sys.version_info < (3,):
    try:
        res = bytearray(result, encoding=locale.getdefaultlocale()[1])
        result = res
    except:
        pass

print(result, end='')

