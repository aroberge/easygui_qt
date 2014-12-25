"""This file is meant to be executed as a subprocess from launcher.pyw"""

import os
import sys

sys.path.insert(0, os.path.join(os.getcwd(), "../"))
func_name = sys.argv[1]
if len(sys.argv)==3:
    locale = sys.argv[2]
else:
    locale = None

try:
    import easygui_qt
    func = getattr(easygui_qt, func_name)
    config = easygui_qt.CONFIG
except:
    try:
        from easygui_qt import easygui_qt
        func = getattr(easygui_qt, func_name)
        config = easygui_qt.CONFIG
    except:
        print("could not find function", func_name)
        sys.exit()

if locale is not None:
    config['locale'] = locale
result = func()

print(result, end='')

