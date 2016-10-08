
===============================
EasyGUI_Qt
===============================

*Inspired by EasyGUI, designed for PyQt*

.. image:: https://raw.githubusercontent.com/aroberge/easygui_qt/master/images/contribute.png


EasyGUI_Qt is a module for simple and easy GUI programming in Python.

EasyGUI_Qt was inspired by EasyGUI created by Stephen Ferg and
is based on Tkinter.  By contrast, EasyGUI_Qt is based on PyQt
which is not included in the standard Python distribution - but is
included in some other distributions like Continuum Analytics' Anaconda.


.. image:: https://badge.fury.io/py/easygui_qt.png
    :target: http://badge.fury.io/py/easygui_qt

.. image:: https://pypip.in/d/easygui_qt/badge.png
        :target: https://pypi.python.org/pypi/easygui_qt

.. image:: https://badge.waffle.io/aroberge/easygui_qt.png?label=ready&title=Ready
 :target: https://waffle.io/aroberge/easygui_qt
 :alt: 'Stories in Ready'


* Free software: BSD license
* Documentation: https://easygui_qt.readthedocs.org.

Python version
--------------

Officially, this is a project that targets only Python 3.  However, I have
now decided to attempt to provide some support for Python 2.  Other than
some unicode issues, all widgets should work with Python 2.

Design philosophy
-----------------

Like the original EasyGUI, EasyGUI_Qt seeks to provide simple GUI widgets
that can be called in a procedural program. EasyGUI_Qt is NOT event-driven: all GUI interactions are invoked
by simple function calls.

The archetype is ``get_string(message)``
which pops a box whose purpose is exactly the same as Python's ``input(prompt)``,
that is, present the user with a question/prompt, have the user enter an
answer, and return the provided answer as a string.  Thus
``easygui_qt.get_string()`` can be used as a drop-in replacement for
``input()``.
Similarly, instead of using a ``print()`` function to display a message,
``show_message()`` is used which pops a message window; however, note that
unlike ``print``, ``show_message`` interrupts the flow of the program
and require some interaction from the user for the program to 
continue.

Unlike the original EasyGUI, which sometimes used cryptic names like
``msgbox`` or ``ynbox``, EasyGUI_Qt attempts to use descriptive names
which follow PEP8 convention.  Thus, instead of ``msgbox``, it uses
``show_message``; instead of ``ynbox``, it has ``get_yes_or_no``.
Most function names start with either ``get_``, ``show_`` or ``set_``.

EasyGUI_QT is based on PyQt; it leverages the available dialogs that
come with PyQt whenever possible.  This makes it possible to have
automatic translation of some GUI elements (such as text on standard buttons)
provided the locale is set correctly and that the local distribution of
PyQt includes the appropriate translation: when EasyGUI_Qt runs, it scans
the standard PyQt location for translation files and note which ones are
present and can be used when the locale is set.

An attempt is made at avoiding duplication of essentially
identical functionality.  Thus, multiple selections from a list of choices
is done only one way: by using a dialog where choices appear as labels
in text and not labels on buttons.

Roadmap
-------

See https://github.com/aroberge/easygui_qt/issues/13 and feel free
to add comments.

Similar projects
----------------

The following is an incomplete lists of a few cross-platform projects
that share some similarity with EasyGUI_Qt, but use back-ends other than PyQt

- `easygui <http://easygui.sourceforge.net/>`_: the original; tkinter back-end
- `anygui <http://anygui.sourceforge.net/>`_: multiple back-ends; well known
  but no longer supported
- `psidialogs <https://github.com/ponty/psidialogs>`_: multiple back-ends supported -
  possibly the most complete project from that point of view.
- `python-dialog <http://pythondialog.sourceforge.net/>`_: dialog/Xdialog/gdialog back-end

There are quite a few lesser known projects but none that seem to be
actively supported.  If you are aware of other projects that should
be mentioned, do not hesitate to contact me and let me know.
