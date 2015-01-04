=================
Naming convention
=================

.. warning:: The naming convention is currently used as a guide helping
             to finalize the API.  Not all widgets listed here are
             implemented yet, or may be implemented using slightly
             different names.

In order to make its use more intuitive, EasyGUI_Qt uses a
consistent naming convention.

All instructions meant to display information to a user
without getting a response back start with ``show``.
The functions available are:

* ``show()``
* ``show_code()``
* ``show_file()``
* ``show_story()``

Note that a detailed description of all of these is given
on the next page.

When a response is expected from the user, the prefixed
used is ``get_``.  Thus we have, in alphabetical order:

* ``get_abort()``
* ``get_button()``
* ``get_choice()``
* ``get_color_hex()``
* ``get_color_rgb()``
* ``get_continue_or_cancel()``
* ``get_date()``
* ``get_directory_name()``
* ``get_file_names()``
* ``get_float()``
* ``get_int()``
* ``get_integer()``
* ``get_language()``
* ``get_list_of_choices()``
* ``get_many_strings()``
* ``get_new_password()``
* ``get_password()``
* ``get_save_file_name()``
* ``get_string()``
* ``get_username_password()``
* ``get_yes_or_no()``


One exception to the above is the special widget used
to handle exceptions, appropriately called:

* ``handle_exception()``

Functions with no corresponding graphical component
can be used to set some global parameters; they
are prefixed by ``set_``:

* ``set_font_size()``
* ``set_language()``

Finally, when writing code, instead of using Python's
``help()`` function, one can simply use following
function which will open the API page on the
ReadTheDocs website:

* ``find_help()``

Specifying arguments
====================

Arguments are all keyword based arguments.  However, in order to enable
simplified entry, they are generally listed in a consistent way.

The first argument is ``message``: this is the text that appears in
the window itself and is usually the most important information that
is conveyed to the user.




