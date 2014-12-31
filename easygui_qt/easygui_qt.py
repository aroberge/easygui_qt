"""EasyGUI_Qt: procedural gui based on PyQt

EasyGUI_Qt is inspired by EasyGUI and contains a number
of different basic graphical user interface components
"""

import collections
import os
import sys
import traceback

if sys.version_info < (3,):
    import ConfigParser as configparser
else:
    import configparser
    unicode = str

from PyQt4 import QtGui, QtCore

try:
    from . import utils
    from . import language_selector
    from . import calendar_widget
    from . import multichoice
    from . import username_password
    from . import change_password
    from . import show_text_window
except:
    import utils
    import language_selector
    import calendar_widget
    import multichoice
    import username_password
    import change_password
    import show_text_window

__all__ = [
    'get_choice',
    'get_list_of_choices',
    'get_float',
    'get_int',
    'get_integer',
    'get_string',
    'get_password',
    'get_username_password',
    'get_new_password',
    'get_yes_or_no',
    'get_continue_or_cancel',
    'get_color_hex',
    'get_color_rgb',
    'get_date',
    'get_directory_name',
    'get_file_names',
    'get_save_file_name',
    'handle_exception',
    'set_font_size',
    'select_language',
    'set_language',
    'show_message',
    'show_file',
    'show_code'
]

QM_FILES = None


class SimpleApp(QtGui.QApplication):
    """A simple extention of the basic QApplication
       with added methods useful for working with dialogs
       that are not class based.
    """

    def __init__(self):
        super(SimpleApp, self).__init__([])

        self.translator = QtCore.QTranslator()
        self.default_font = QtGui.QFont()

        if sys.version_info < (3,) :
            settings_path = ".easygui-qt2"
        else:
            settings_path = ".easygui-qt3"
        self.config_path = os.path.join(os.path.expanduser("~"),
                                         settings_path)
        try:
            self.load_config()
            self.setFont(self.default_font)
        except:
            pass

        self.save_config()

    def save_config(self):
        config = configparser.RawConfigParser()
        config.add_section('Configuration')
        config.set('Configuration', 'locale', self.config['locale'])
        config.set('Configuration', 'font-size', self.config['font-size'])
        with open(self.config_path, 'w') as configfile:
            config.write(configfile)

    def load_config(self):
        # Todo: make more robust
        config = configparser.RawConfigParser()
        self.config = {}
        try:
            config.read(self.config_path)
            self.config['locale'] = config.get('Configuration', 'locale')
            self.set_locale(self.config['locale'], save=False)
            self.config['font-size'] = config.getint('Configuration', 'font-size')
            self.set_font_size(self.config['font-size'], save=False)
        except:
            print("Proble encountered in load_config.")
            self.config = {'locale': 'default', 'font-size': 12}
            return

    def set_locale(self, locale, save=True):
        """Sets the language of the basic controls for PyQt
           from a locale - provided that the corresponding qm files
           are present in the PyQt distribution.
        """
        global QM_FILES
        if QM_FILES is None:
            QM_FILES = utils.find_qm_files()
        if locale in QM_FILES:
            if self.translator.load("qt_" + locale, QM_FILES[locale]):
                self.installTranslator(self.translator)
                self.config['locale'] = locale
            else:
                print("language not available")
        elif locale == "default" and self.config['locale'] != 'default':
            self.removeTranslator(self.translator)
            self.translator = QtCore.QTranslator()
            self.config['locale'] = 'default'
        elif self.config['locale'] in QM_FILES:
            if self.translator.load("qt_" + self.config['locale'],
                                         QM_FILES[self.config['locale']]):
                self.installTranslator(self.translator)
        if save:
            self.save_config()

    def set_font_size(self, font_size, save=True):
        """Internal method to set font size.
        """
        try:
            font_size = int(font_size)
        except:
            print("font_size should be an integer")
            return
        self.default_font.setPointSize(font_size)
        self.config['font-size'] = font_size
        self.setFont(self.default_font)
        if save:
            self.save_config()

#========== Message Boxes ====================#

def show_message(message="Message", title="Title"):
    """Simple message box.

       :param message: message string
       :param title: window title

       >>> import easygui_qt as easy
       >>> easy.show_message()

       .. image:: ../docs/images/show_message.png
    """
    app = SimpleApp()
    box = QtGui.QMessageBox(None)
    box.setWindowTitle(title)
    box.setText(message)
    box.show()
    box.raise_()
    box.exec_()
    app.quit()


def get_yes_or_no(question="Answer this question", title="Title"):
    """Simple yes or no question.

       :param question: Question (string) asked
       :param title: Window title (string)

       :return: ``True`` for "Yes", ``False`` for "No",
               and ``None`` for "Cancel".

       >>> import easygui_qt as easy
       >>> choice = easy.get_yes_or_no()

       .. image:: ../docs/images/yes_no_question.png
    """
    app = SimpleApp()
    flags = QtGui.QMessageBox.Yes | QtGui.QMessageBox.No
    flags |= QtGui.QMessageBox.Cancel

    box = QtGui.QMessageBox()
    box.show()
    box.raise_()

    reply = box.question(None, title, question, flags)
    app.quit()
    if reply == QtGui.QMessageBox.Yes:
        return True
    elif reply == QtGui.QMessageBox.No:
        return False


def get_continue_or_cancel(question="Processed will be cancelled!",
                           title="Title"):
    """Continue or cancel question, shown as a warning (i.e. more urgent than
       simple message)

       :param question: Question (string) asked
       :param title: Window title (string)

       :return: "continue" for "No, please continue",
                "cancel" for "Cancel" (or dismissing the dialog)

       >>> import easygui_qt as easy
       >>> choice = easy.get_continue_or_cancel()

       .. image:: ../docs/images/get_continue_or_cancel.png
    """
    app = SimpleApp()
    message_box = QtGui.QMessageBox(QtGui.QMessageBox.Warning, title, question,
                                    QtGui.QMessageBox.NoButton)
    message_box.addButton("No, please continue", QtGui.QMessageBox.AcceptRole)
    message_box.addButton("Cancel", QtGui.QMessageBox.RejectRole)
    message_box.show()
    message_box.raise_()

    if message_box.exec_() == QtGui.QMessageBox.AcceptRole:
        app.quit()
        return "continue"
    else:
        app.quit()
        return "cancel"

#============= Color dialogs =================

def get_color_hex():
    """Using a color dialog, returns a color in hexadecimal notation
       i.e. a string '#RRGGBB' or "None" if color dialog is dismissed.

       >>> import easygui_qt as easy
       >>> color = easy.get_color_hex()

       .. image:: ../docs/images/select_color.png
       """
    app = SimpleApp()
    color = QtGui.QColorDialog.getColor(QtCore.Qt.white, None)
    app.quit()
    if color.isValid():
        return color.name()

def get_color_rgb(app=None):
    """Using a color dialog, returns a color in rgb notation
       i.e. a tuple (r, g, b)  or "None" if color dialog is dismissed.

       >>> import easygui_qt as easy
       >>> easy.set_language('fr')
       >>> color = easy.get_color_rgb()

       .. image:: ../docs/images/select_color_fr.png
       """
    app = SimpleApp()
    color = QtGui.QColorDialog.getColor(QtCore.Qt.white, None)
    app.quit()
    if color.isValid():
        return (color.red(), color.green(), color.blue())

#================ Date ===================

def get_date(title="Select Date"):
    """Calendar widget

       :param title: window title
       :return: the selected date as a string

       >>> import easygui_qt as easy
       >>> date = easy.get_date()

       .. image:: ../docs/images/get_date.png
    """
    app = SimpleApp()
    cal = calendar_widget.CalendarWidget(title=title)
    app.exec_()
    date = cal.date.toString()
    if sys.version_info < (3,):
        return unicode(date)
    return date

#================ language/locale related

def select_language(title="Select language", name="Language codes",
                    instruction=None):
    """Dialog to choose language based on some locale code for
       files found on default path.

       :param title: Window title
       :param name: Heading for valid values of locale appearing in checkboxes
       :param instruction: Like the name says; when set to None, a default
                        string is used which includes the current language used.

       The first time an EasyGUI_Qt widget is created in a program, the
       PyQt language files found in the standard location of the user's computer
       are scanned and recorded; these provide some translations of standard
       GUI components (like name of buttons).  Note that "en" is not found
       as a locale (at least, not on the author's computer) but using "default"
       reverts the choice to the original (English here).

       >>> import easygui_qt as easy
       >>> easy.select_language()

       .. image:: ../docs/images/select_language.png
    """
    app = SimpleApp()
    if instruction is None:
        instruction = ('Current language code is "{}".'.format(
                                                        app.config['locale']))
    selector = language_selector.LanguageSelector(app, title=title, name=name,
                                 instruction=instruction)
    selector.exec_()
    app.quit()


def set_language(locale):
    """Sets the locale, if available

       :param locale: standard code for locale (e.g. 'fr', 'en_CA')

       Does not create a GUI widget, but affect the appearance of
       widgets created afterwards

       >>> import easygui_qt as easy
       >>> easy.set_locale('es')

       >>> # after setting the locale
       >>> easy.get_yes_or_no()

       .. image:: ../docs/images/after_set_locale.png

    """
    app = SimpleApp()
    app.set_locale(locale)
    app.quit()
    return locale


#=========== InputDialogs ========================

def get_common_input_flags():
    '''avoiding copying same flags in all functions'''
    flags = QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint
    flags |= QtCore.Qt.WindowStaysOnTopHint
    return flags

class VisibleInputDialog(QtGui.QInputDialog):
    '''A simple InputDialog class that attempts to make itself automatically
       on all platforms
    '''
    def __init__(self):
        super(VisibleInputDialog, self).__init__()
        self.show()
        self.raise_()


def get_int(message="Choose a number", title="Title",
                  default_value=1, min_=0, max_=100, step=1):
    """Simple dialog to ask a user to select an integer within a certain range.

       **Note**: **get_int()** and **get_integer()** are identical.

       :param message: Message displayed to the user, inviting a response
       :param title: Window title
       :param default_value: Default value for integer appearing in the text
                             box; set to the closest of ``min_`` or ``max_``
                             if outside of allowed range.
       :param min_: Minimum integer value allowed
       :param max_: Maximum integer value allowed
       :param step: Indicate the change in integer value when clicking on
                    arrows on the right hand side

       :return: an integer, or ``None`` if "cancel" is clicked or window
                is closed.

       >>> import easygui_qt as easy
       >>> number = easy.get_int()

       .. image:: ../docs/images/get_int.png


       If ``default_value`` is larger than ``max_``, it is set to ``max_``;
       if it is smaller than ``min_``, it is set to ``min_``.

       >>> number = easy.get_integer("Enter a number", default_value=125)

       .. image:: ../docs/images/get_int2.png

    """
    # converting values to int for launcher demo set_font_size which
    # first queries the user for a value; the initial values are passed
    # as strings by the subprocess module and need to be converted here

    default_value = int(default_value)
    min_ = int(min_)
    max_ = int(max_)

    app = SimpleApp()
    dialog = VisibleInputDialog()
    flags = get_common_input_flags()
    number, ok = dialog.getInteger(None, title, message,
                                   default_value, min_, max_, step,
                                   flags)
    dialog.destroy()
    app.quit()
    if ok:
        return number
get_integer = get_int


def get_float(message="Choose a number", title="Title", default_value=0.0,
                                min_=-10000, max_=10000, decimals=3):
    """Simple dialog to ask a user to select a floating point number
       within a certain range and a maximum precision.

       :param message: Message displayed to the user, inviting a response
       :param title: Window title
       :param default_value: Default value for value appearing in the text
                             box; set to the closest of ``min_`` or ``max_``
                             if outside of allowed range.
       :param min_: Minimum value allowed
       :param max_: Maximum value allowed
       :param decimals: Indicate the maximum decimal precision allowed

       :return: a floating-point number, or ``None`` if "cancel" is clicked
                or window is closed.

       >>> import easygui_qt as easy
       >>> number = easy.get_float()

       .. image:: ../docs/images/get_float.png

       **Note:** depending on the locale of the operating system where
       this is used, instead of a period being used for indicating the
       decimals, a comma may appear instead; this is the case for
       the French version of Windows for example.  Therefore, entry of
       floating point values in this situation will require the use
       of a comma instead of a period.  However, the internal representation
       will still be the same, and the number passed to Python will be
       using the familar notation.
    """
    app = SimpleApp()
    dialog = VisibleInputDialog()
    flags = get_common_input_flags()
    number, ok = dialog.getDouble(None, title, message,
                                  default_value, min_, max_, decimals,
                                  flags)
    app.quit()
    if ok:
        return number


def get_string(message="Enter your response", title="Title",
               default_response=""):
    """Simple text input box.  Used to query the user and get a string back.

       :param message: Message displayed to the user, inviting a response
       :param title: Window title
       :param default_response: default response appearing in the text box

       :return: a string, or ``None`` if "cancel" is clicked or window
                is closed.

       >>> import easygui_qt as easy
       >>> reply = easy.get_string()

       .. image:: ../docs/images/get_string.png

       >>> reply = easy.get_string("new message", default_response="ready")

       .. image:: ../docs/images/get_string2.png
    """
    app = SimpleApp()
    dialog = VisibleInputDialog()
    flags = get_common_input_flags()
    text, ok = dialog.getText(None, title, message, QtGui.QLineEdit.Normal,
                              default_response, flags)
    app.quit()
    if ok:
        if sys.version_info < (3,):
            return unicode(text)
        return text


def get_password(message="Enter your password", title="Title"):
    """Simple password input box.  Used to query the user and get a string back.

       :param message: Message displayed to the user, inviting a response
       :param title: Window title


       :return: a string, or ``None`` if "cancel" is clicked or window
                is closed.

       >>> import easygui_qt as easy
       >>> password = easy.get_password()

       .. image:: ../docs/images/get_password.png
    """
    app = SimpleApp()
    dialog = VisibleInputDialog()
    flags = get_common_input_flags()
    text, ok = dialog.getText(None, title, message, QtGui.QLineEdit.Password,
                              '', flags)
    app.quit()
    if ok:
        if sys.version_info < (3,):
            return unicode(text)
        return text


def get_choice(message="Select one item", title="Title", choices=None):
    """Simple dialog to ask a user to select an item within a drop-down list

       :param message: Message displayed to the user, inviting a response
       :param title: Window title
       :param choices: iterable (list or tuple) containing the names of
                       the items that can be selected.

       :returns: a string, or ``None`` if "cancel" is clicked or window
                is closed.

       >>> import easygui_qt as easy
       >>> choices = ["CPython", "Pypy", "Jython", "IronPython"]
       >>> reply = easy.get_choice("What is the best Python implementation",
       ...                         choices=choices)

       .. image:: ../docs/images/get_choice.png
    """
    if choices is None:
        choices = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
    app = SimpleApp()
    dialog = VisibleInputDialog()
    flags = get_common_input_flags()
    choice, ok = dialog.getItem(None, title, message, choices, 0, False, flags)
    app.quit()
    if ok:
        if sys.version_info < (3,):
            return unicode(choice)
        return choice


def get_username_password(title="title", fields=None):
    """User name and password input box.

       :param title: Window title
       :param fields: an iterable containing the labels for "user name"
                      and "password" - useful for languages other than English


       :return: An ordered dict containing the fields item as keys, and
                the input from the user (empty string by default) as value

       >>> import easygui_qt as easy
       >>> reply = easy.get_username_password()
       >>> reply
       OrderedDict([('User name', 'aroberge'), ('Password', 'not a good password')])

       .. image:: ../docs/images/get_username_password.png
    """
    class Info:
        o_dict = collections.OrderedDict()
    info = Info()
    if fields is None:
        info.o_dict["User name"] = ''
        info.o_dict["Password"] = ''
    else:
        for item in fields:
            info.o_dict[item] = ''
    app = SimpleApp()
    unp = username_password.UserNamePassword(info)
    unp.exec_()
    app.quit()
    return info.o_dict

def get_new_password(title="title", fields=None, verification=None):
    """Change password input box.

       :param title: Window title
       :param fields: an iterable containing the labels for "Old password"
                      and "New password" and "Confirm new password". All
                      three labels must be different strings as they are used
                      as keys in a dict - however, they could differ only by
                      a space.
       :param verification: a custom method used to verify if the new password
                            is acceptable. **This method must return ``None``**
                            if the new password are to be accepted.
                            An example of such a method is given below.


       :return: An ordered dict containing the fields item as keys, and
                the input from the user as values. If the verification is
                not satisfied, then the values are set to blank strings.
                Note that the verification method could, if desired,
                alter the values that are sent back - they could be hashed
                for instance.

       >>> import easygui_qt as easy
       >>> reply = easy.get_new_password()

       .. image:: ../docs/images/get_new_password.png

       Example of a verification function::

        def verification(self):
            '''Silly demo of a verification function.  It requires that the
               original password be "password" and that the two new passwords
               be identical.
            '''
            message = None
            o_dict = self.parent.o_dict
            if o_dict[self.keys[0]] != "password":
                message = ("Original password does not match expected value "+
                           "[Hint: it's 'password']")
                self.show_message(message)
            elif o_dict[self.keys[1]] != o_dict[self.keys[2]]:
                message = "New password values must be identical."
                self.show_message(message)
            return message
    """
    class Parent:
        o_dict = collections.OrderedDict()
    parent = Parent()
    if fields is None:
        parent.o_dict["Old password:"] = ''
        parent.o_dict["New password:"] = ''
        parent.o_dict["Confirm new password:"] = ''
    else:
        for item in fields:
            parent.o_dict[item] = ''
    app = SimpleApp()
    ch_pwd = change_password.ChangePassword(parent)
    ch_pwd.exec_()
    app.quit()
    return parent.o_dict


def get_list_of_choices(title="Title", choices=None):
    """Show a list of possible choices to be selected.

       :param title: Window title
       :param choices: iterable (list, tuple, ...) containing the choices as
                       strings

       :returns: a list of selected items, otherwise an empty list.

       >>> import easygui_qt as easy
       >>> choices = easy.get_list_of_choices()

       .. image:: ../docs/images/get_list_of_choices.png
    """
    app = SimpleApp()
    dialog = multichoice.MultipleChoicesDialog(title=title, choices=choices)
    dialog.exec_()
    app.quit()
    if sys.version_info < (3,):
        return [unicode(item) for item in dialog.selection]
    return dialog.selection

#========== Files & directory dialogs


def get_directory_name(title="Get directory"):
    '''Gets the name (full path) of an existing directory

       :param title: Window title
       :return: the name of a directory or an empty string if cancelled.

       >>> import easygui_qt as easy
       >>> easy.get_directory_name()

       .. image:: ../docs/images/get_directory_name.png

       By default, this dialog initially displays the content of the current
       working directory.
    '''
    app = SimpleApp()
    options = QtGui.QFileDialog.Options()
    # Without the following option (i.e. using native dialogs),
    # calling this function twice in a row made Python crash.
    options |= QtGui.QFileDialog.DontUseNativeDialog
    options |= QtGui.QFileDialog.DontResolveSymlinks
    options |= QtGui.QFileDialog.ShowDirsOnly
    directory = QtGui.QFileDialog.getExistingDirectory(None,
                                            title, os.getcwd(), options)
    app.quit()
    if sys.version_info < (3,):
        return unicode(directory)
    return directory


def get_file_names(title="Get existing file names"):
    '''Gets the names (full path) of existing files

       :param title: Window title
       :return: the list of names (paths) of files selected.
               (It can be an empty list.)

       >>> import easygui_qt as easy
       >>> easy.get_file_names()

       .. image:: ../docs/images/get_file_names.png

       By default, this dialog initially displays the content of the current
       working directory.
    '''
    app = SimpleApp()
    if sys.version_info < (3,):
        files = QtGui.QFileDialog.getOpenFileNames(None, title, os.getcwd(),
                                               "All Files (*.*)")
        files = [unicode(item) for item in files]
    else:
        options = QtGui.QFileDialog.Options()
        options |= QtGui.QFileDialog.DontUseNativeDialog
        files = QtGui.QFileDialog.getOpenFileNames(None, title, os.getcwd(),
                                               "All Files (*.*)", options)
    app.quit()
    return files


def get_save_file_name(title="File name to save"):
    '''Gets the name (full path) of of a file to be saved.

       :param title: Window title
       :return: the name (path) of file selected

       The user is warned if the file already exists and can choose to
       cancel.  However, this dialog actually does NOT save any file: it
       only return a string containing the full path of the chosen file.

       >>> import easygui_qt as easy
       >>> easy.get_save_file_name()

       .. image:: ../docs/images/get_save_file_name.png

       By default, this dialog initially displays the content of the current
       working directory.
    '''
    app = SimpleApp()
    if sys.version_info < (3,):
        file_name = QtGui.QFileDialog.getSaveFileName(None, title, os.getcwd(),
                                               "All Files (*.*)")
        app.quit()
        return unicode(file_name)

    options = QtGui.QFileDialog.Options()
    options |= QtGui.QFileDialog.DontUseNativeDialog  # see get_directory_name
    file_name = QtGui.QFileDialog.getSaveFileName(None, title, os.getcwd(),
                                               "All Files (*.*)", options)
    app.quit()
    return file_name

#========= Font related

def set_font_size(font_size):
    """Simple method to set font size.

    :param font_size: integer value

    Does not create a GUI widget; but affects the appearance of
    future GUI widgets.

    >>> import easygui_qt as easy
    >>> easy.set_font_size(20)
    >>> easy.show_message()

    .. image:: ../docs/images/set_font_size.png
    """
    app = SimpleApp()
    app.set_font_size(font_size)
    app.quit()
    print(font_size)  # info for launcher

def show_file(title="title", file_name=None, html=False):
    '''Displays a file in a window.  While it looks as though the file
       can be edited, the only changes that happened are in the window
       and nothing can be saved.

       :param title: the window title
       :param file_name: the file name, relative to the calling program
       :param html: indicates if the file is an html document.

       When html is set to True, the file is formatted assuming
       it uses html syntax.  Otherwise, it formats it in a
       monospace font and, if the file name ends with
       "py" or "pyw", some code highlighting is done.

       **Note**: a better hightlighter would be most welcome!

       >>> import easygui_qt as easy
       >>> easy.show_file()

       .. image:: ../docs/images/show_file.png
    '''
    app = SimpleApp()
    editor = show_text_window.TextWindow(title=title, file_name=file_name,
                                         html=html)
    editor.show()
    app.exec_()

def show_code(title="title", code=None):
    '''Displays some text in a window, in a monospace file.

       :param title: the window title
       :param code: a string to display in the window.

       >>> import easygui_qt as easy
       >>> easy.show_code()

       .. image:: ../docs/images/show_code.png
    '''
    app = SimpleApp()
    editor = show_text_window.TextWindow(title=title, code=code)
    editor.resize(720, 450)
    editor.show()
    app.exec_()

def handle_exception(title="Exception raised!"):
    '''Displays a traceback in a window if an exception is raised.
       If the user clicks on "abort", sys.exit() is called and the
       program ends.  If the user clicks on "ignore", the program
       resumes its execution.

       :param title: the window title

       .. image:: ../docs/images/handle_exception.png
    '''
    try:
        message = "\n".join(traceback.format_exception(sys.exc_info()[0],
                        sys.exc_info()[1] , sys.exc_info()[2]))
    except AttributeError:
        return "No exception was raised"

    app = SimpleApp()
    reply = QtGui.QMessageBox.critical(None, title, message,
            QtGui.QMessageBox.Abort | QtGui.QMessageBox.Ignore)
    if reply == QtGui.QMessageBox.Abort:
        sys.exit()
    else:
        pass
    app.quit()

if __name__ == '__main__':
    try:
        from demos import guessing_game
        guessing_game.guessing_game()
    except ImportError:
        print("Could not find demo.")
