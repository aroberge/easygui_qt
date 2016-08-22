.. :changelog:

History
=======

0.9.2
-----

(Some of the changes noted are addition or improvements submitted by David Hughes via email)

- TextWindow now shows input either from a file or from a supplied string.
- added show_code()
- added show_text()
- renamed show() to show_message() [reverting change from 0.9.1]
- started creation of custom "page format" for more complex dialogs
- changed get_date() so that it returns a datetime date instance

Note: the documentation has NOT been updated to reflect these changes.

0.9.1
-----

- removed verification from get_new_password
- added find_help
- created "back end" for wizard creator - will become show_story()
- documented and changed naming convention
- renamed select_language() : get_language()
- renamed show_message() : show()
- fixed a unicode bug for Python 2
- changed the way show_file works
- removed required_install PyQt4 from setup.py

0.9.0a
------

- Simplified the way change_password was implemented by reusing one of
  the new modules and fixed an unreported bug in the process
- changed the formatting of this file so that it should not cause problems
  with PyPI anymore.


0.9.0
-----

Major change in version number as almost all the desired widgets for
version 1.0 have been implemented.

Release notes:
--------------

Some unicode problems are likely present when using Python 2.7; the primary
target is Python 3.3+ ... but we try to support earlier version as well.

Some problems are present with Mac OSX and Python 2.7 (only?)


- added show_abort
- added get_many_strings
- added handle_exception
- added show_code
- added show_file
- added get_new_password
- adressed an issue where some dialogs would appear below some windows
  (e.g. terminal) when launched from some platforms (e.g. Mac OSX):
  the goal should be that the dialogs always appear on top of other windows.
- removed with_app decorator; this decorator had been introduced to reduce
  the amount of repetitive code appearing in each function (and initially
  inspected the function signature to add automatically some additional
  keyword args) but it likely made it impossible to do unit testing with
  QTest (still not done) and prevented ReadTheDocs from reading the correct
  signatures for the decorated functions.
- tooltips added to demos launcher
- added get_username_password

0.4.0
-----

- added get_password
- added get_date
- added get_color_hex
- added get_color_rgb
- added get_continue_or_cancel
- added roadmap as a github issue https://github.com/aroberge/easygui_qt/issues/13
- removed CONFIG as a global dict; using the configuration file instead.
- remove set_default_font
- rename set_locale to set_language
- added configuration file to save locale and font size

0.3.0
-----

- Decided to support (with lower priority) Python 2  (2.7.9 more specifically)
- Should work reasonably well with Python 2.7.9 - other than potential
  unicode related issues
- made get_list_of_choices(), get_choice(), get_string(), and get_directory_name()
  work properly with Python 2.7.9

0.2.3a
------

- changed extension of some demos (from .pyw to .py) as they were not uploaded to pypi

0.2.3
-----

- added demos dir to setup.py so that it can be included on pypi

0.2.2a
------

- changing path on image in readme in attempt to help pypi display properly

0.2.2
-----

- changed the syntax for calls to super() to be compatible with Python 2.
  Note that the intention is to be a Python 3 project, but if simple changes
  can make it compatible with Python 2, they will be incorporated.
- changed name of set_save_file_name to get_save_file_name
- changed name of yes_no_question to get_yes_or_no
- added get_list_of_choices
- added demo launcher

0.2.1
-----

- Moved the demos directory to a more sensible location
- added get_directory_name
- added get_file_names
- added set_save_file_name
- attempt to fix bug for Python 3.2 where inspect.signature was not defined

0.2.0
------

The API has been changed since the initial release
and the following widgets have been documented, with images inserted
in the documentation.

- get_choice
- get_float
- get_int
- get_integer
- get_string
- set_font_size
- set_default_font
- select_language
- set_locale
- show_message
- yes_no_question

0.1.0
---------------------

* First release on PyPI.
