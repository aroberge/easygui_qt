"""This file is meant to be executed as a subprocess from launcher.pyw"""

import os
import sys

sys.path.insert(0, os.path.join(os.getcwd(), "../"))
func_name = sys.argv[1]

try:
    import easygui_qt
    func = getattr(easygui_qt, func_name)
except:
    try:
        from easygui_qt import easygui_qt
        func = getattr(easygui_qt, func_name)
    except:
        print("could not find function", func_name)
        sys.exit()

result = func()

print(result, end='')

