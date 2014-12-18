import os
import sys
sys.path.insert(0, os.getcwd())

try:
    from easygui_qt import easygui_qt
except ImportError:
    print("problem with import")

name = easygui_qt.text_input(message="What is your name?",
                            title="Mine is Reeborg.")

print(name, end='')

