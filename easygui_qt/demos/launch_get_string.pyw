import os
import sys
sys.path.insert(0, os.path.join(os.getcwd(), "../"))

try:
    from easygui_qt import get_string
except:
    from easygui_qt.easygui_qt import get_string

name = get_string()

print(name, end='')

