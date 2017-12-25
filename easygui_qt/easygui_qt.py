"""EasyGUI_Qt: procedural gui based on PyQt

EasyGUI_Qt is inspired by EasyGUI and contains a number
of different basic graphical user interface components
"""
import os
import sys
import traceback
import webbrowser

if sys.version_info < (3,):
    import ConfigParser as configparser
else:
    import configparser
    unicode = str

try:
    from PyQt4 import QtGui, QtCore
    qt_widgets = QtGui
    _qt4 = True
except ImportError:
    from PyQt5 import QtGui, QtCore
    from PyQt5 import QtWidgets as qt_widgets
    _qt4 = False


try:
    from . import utils
    from . import language_selector
    from . import calendar_widget
    from . import multichoice
    from . import show_text_window
    from . import multifields
except:
    import utils
    import language_selector
    import calendar_widget
    import multichoice
    import show_text_window
    import multifields


__all__ = [
    'get_choice',
    'get_list_of_choices',
    'get_float',
    'get_int',
    'get_integer',
    'get_string',
    'get_many_strings',
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
    'get_language',
    'set_language',
    'get_abort',
    'show_message',    
    'show_file',
    'show_text',
    'show_code',
    'show_html',
    'find_help'
]

QM_FILES = None


class SimpleApp(qt_widgets.QApplication):
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
            print("Problem encountered in load_config.")
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
def show_message(message="Message",
                 title="Title"):
    """Simple message box.

       :param message: message string
       :param title: window title

       >>> import easygui_qt as easy
       >>> easy.show_message()

       .. image:: ../docs/images/show_message.png
    """
    app = SimpleApp()
    box = qt_widgets.QMessageBox(None)
    box.setWindowTitle(title)
    box.setText(message)
    box.show()
    box.raise_()
    box.exec_()
    app.quit()


def get_yes_or_no(message="Answer this question", title="Title"):
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
    flags = qt_widgets.QMessageBox.Yes | qt_widgets.QMessageBox.No
    flags |= qt_widgets.QMessageBox.Cancel

    box = qt_widgets.QMessageBox()
    box.show()
    box.raise_()

    reply = box.question(None, title, message, flags)
    app.quit()
    return reply == qt_widgets.QMessageBox.Yes


def get_continue_or_cancel(message="Processed will be cancelled!",
                           title="Title",
                           continue_button_text="Continue",
                           cancel_button_text="Cancel"):
    """Continue or cancel question, shown as a warning (i.e. more urgent than
       simple message)

       :param question: Question (string) asked
       :param title: Window title (string)
       :param continue_button_text: text to display on button
       :param cancel_button_text: text to display on button

       :return: True for "Continue", False for "Cancel"

       >>> import easygui_qt as easy
       >>> choice = easy.get_continue_or_cancel()

       .. image:: ../docs/images/get_continue_or_cancel.png
    """
    app = SimpleApp()
    message_box = qt_widgets.QMessageBox(qt_widgets.QMessageBox.Warning, title, message,
                                    qt_widgets.QMessageBox.NoButton)
    message_box.addButton(continue_button_text, qt_widgets.QMessageBox.AcceptRole)
    message_box.addButton(cancel_button_text, qt_widgets.QMessageBox.RejectRole)
    message_box.show()
    message_box.raise_()

    reply = message_box.exec_()
    app.quit()
    return reply == qt_widgets.QMessageBox.AcceptRole


#============= Color dialogs =================

def get_color_hex():
    """Using a color dialog, returns a color in hexadecimal notation
       i.e. a string '#RRGGBB' or "None" if color dialog is dismissed.

       >>> import easygui_qt as easy
       >>> color = easy.get_color_hex()

       .. image:: ../docs/images/select_color.png
       """
    app = SimpleApp()
    color = qt_widgets.QColorDialog.getColor(QtCore.Qt.white, None)
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
    color = qt_widgets.QColorDialog.getColor(QtCore.Qt.white, None)
    app.quit()
    if color.isValid():
        return (color.red(), color.green(), color.blue())

#================ Date ===================

def get_date(title="Select Date"):
    """Calendar widget

       :param title: window title
       :return: the selected date as a ``datetime.date`` instance

       >>> import easygui_qt as easy
       >>> date = easy.get_date()

       .. image:: ../docs/images/get_date.png
    """
    app = SimpleApp()
    cal = calendar_widget.CalendarWidget(title=title)
    app.exec_()
    date = cal.date.toPyDate()
    return date

#================ language/locale related

def get_language(title="Select language", name="Language codes",
                    instruction=None):
    """Dialog to choose language based on some locale code for
       files found on default path.

       :param title: Window title
       :param name: Heading for valid values of locale appearing in checkboxes
       :param instruction: Like the name says; when set to None, a default
                       string is used which includes the current language used.

       The first time an EasyGUI_Qt widget is created in a program, the PyQt
       language files found in the standard location of the user's computer
       are scanned and recorded; these provide some translations of standard
       GUI components (like name of buttons).  Note that "en" is not found
       as a locale (at least, not on the author's computer) but using "default"
       reverts the choice to the original (English here).

       >>> import easygui_qt as easy
       >>> easy.get_language()

       .. image:: ../docs/images/get_language.png
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

class VisibleInputDialog(qt_widgets.QInputDialog):
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
    if _qt4:
        number, ok = dialog.getInteger(None, title, message,
                                   default_value, min_, max_, step,
                                   flags)
    else:
        number, ok = dialog.getInt(None, title, message,
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
    text, ok = dialog.getText(None, title, message, qt_widgets.QLineEdit.Normal,
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
    text, ok = dialog.getText(None, title, message, qt_widgets.QLineEdit.Password,
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


def get_username_password(title="Title", labels=None):
    """User name and password input box.

       :param title: Window title
       :param labels: an iterable containing the labels for "user name"
                      and "password"; if the value not specified, the
                      default values will be used.

       :return: An ordered dict containing the fields item as keys, and
                the input from the user (empty string by default) as value

       Note: this function is a special case of ``get_many_strings`` where
       the required masks are provided automatically..

       >>> import easygui_qt as easy
       >>> reply = easy.get_username_password()
       >>> reply
       OrderedDict([('User name', 'aroberge'), ('Password', 'not a good password')])

       .. image:: ../docs/images/get_username_password.png
    """
    if labels is None:
        labels = ["User name", "Password"]
    if len(labels) != 2:
        _title = "Error found"
        message = "labels should have 2 elements; {} were found".format(len(labels))
        get_abort(title=_title, message=message)
    masks = [False, True]
    return get_many_strings(title=title, labels=labels, masks=masks)


def get_new_password(title="Title", labels=None):
    """Change password input box.

       :param title: Window title
       :param labels: an iterable containing the labels for "Old password"
                      and "New password" and "Confirm new password". All
                      three labels must be different strings as they are used
                      as keys in a dict - however, they could differ only by
                      a space.

       :return: An ordered dict containing the fields item as keys, and
                the input from the user as values.

       Note: this function is a special case of ``get_many_strings`` where
       the required masks are provided automatically..

       >>> import easygui_qt as easy
       >>> reply = easy.get_new_password()

       .. image:: ../docs/images/get_new_password.png
    """

    if not labels:  # empty list acceptable for test
        labels = ["Old password:", "New password:", "Confirm new password:"]
    if len(labels) != 3:
        _title = "Error found"
        message = "labels should have 3 elements; {} were found".format(len(labels))
        get_abort(title=_title, message=message)
    masks = [True, True, True]
    class Parent:
        pass
    parent = Parent()
    app = SimpleApp()
    dialog = multifields.MultipleFieldsDialog(labels=labels, masks=masks,
                                              parent=parent, title=title)
    dialog.exec_()
    app.quit()
    return parent.o_dict

def get_many_strings(title="Title", labels=None, masks=None):
    """Multiple strings input

       :param title: Window title
       :param labels: an iterable containing the labels for to use for the entries
       :param masks: optional parameter.


       :return: An ordered dict containing the labels as keys, and
                the input from the user (empty string by default) as value

       The parameter ``masks`` if set must be an iterable of the same
       length as ``choices`` and contain either True or False as entries
       indicating if the entry of the text is masked or not.  For example,
       one could ask for a username and password using get_many_strings
       as follows [note that get_username_password exists and automatically
       takes care of specifying the masks and is a better choice for this
       use case.]

       >>> import easygui_qt as easy
       >>> labels = ["User name", 'Password']
       >>> masks = [False, True]
       >>> reply = easy.get_many_strings(labels=labels, masks=masks)
       >>> reply
       OrderedDict([('User name', 'aroberge'), ('Password', 'not a good password')])

       .. image:: ../docs/images/get_many_strings.png
    """
    class Parent:
        pass
    parent = Parent()
    app = SimpleApp()
    dialog = multifields.MultipleFieldsDialog(labels=labels, masks=masks,
                                              parent=parent, title=title)
    dialog.exec_()
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
    options = qt_widgets.QFileDialog.Options()
    # Without the following option (i.e. using native dialogs),
    # calling this function twice in a row made Python crash.
    options |= qt_widgets.QFileDialog.DontUseNativeDialog
    options |= qt_widgets.QFileDialog.DontResolveSymlinks
    options |= qt_widgets.QFileDialog.ShowDirsOnly
    directory = qt_widgets.QFileDialog.getExistingDirectory(None,
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
        files = qt_widgets.QFileDialog.getOpenFileNames(None, title, os.getcwd(),
                                               "All Files (*.*)")
        files = [unicode(item) for item in files]
    else:
        options = qt_widgets.QFileDialog.Options()
        options |= qt_widgets.QFileDialog.DontUseNativeDialog
        files = qt_widgets.QFileDialog.getOpenFileNames(None, title, os.getcwd(),
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
        file_name = qt_widgets.QFileDialog.getSaveFileName(None, title, os.getcwd(),
                                               "All Files (*.*)")
        app.quit()
        return unicode(file_name)

    options = qt_widgets.QFileDialog.Options()
    options |= qt_widgets.QFileDialog.DontUseNativeDialog  # see get_directory_name
    file_name = qt_widgets.QFileDialog.getSaveFileName(None, title, os.getcwd(),
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

def show_file(file_name=None, title="Title", file_type="text"):
    '''Displays a file in a window.  While it looks as though the file
       can be edited, the only changes that happened are in the window
       and nothing can be saved.

       :param title: the window title
       :param file_name: the file name, (path) relative to the calling program
       :param file_type: possible values: ``text``, ``code``, ``html``, ``python``.

       By default, file_type is assumed to be ``text``; if set to ``code``,
       the content is displayed with a monospace font and, if
       set to ``python``, some code highlighting is done.
       If the file_type is ``html``, it is processed assuming it follows
       html syntax.

       **Note**: a better Python code hightlighter would be most welcome!

       >>> import easygui_qt as easy
       >>> easy.show_file()

       .. image:: ../docs/images/show_file.png
    '''
    app = SimpleApp()
    editor = show_text_window.TextWindow(file_name=file_name,
                                         title=title,
                                         text_type=file_type)
    editor.show()
    app.exec_()

    
def show_text(title="Title", text=""):
    '''Displays some text in a window.

       :param title: the window title
       :param code: a string to display in the window.

       >>> import easygui_qt as easy
       >>> easy.show_code()

       .. image:: ../docs/images/show_text.png
    '''
    app = SimpleApp()
    editor = show_text_window.TextWindow(title=title, text_type='text', text=text)
    editor.resize(720, 450)
    editor.show()
    app.exec_()

    
def show_code(title="Title", text=""):
    '''Displays some text in a window, in a monospace font.

       :param title: the window title
       :param code: a string to display in the window.

       >>> import easygui_qt as easy
       >>> easy.show_code()

       .. image:: ../docs/images/show_code.png
    '''
    app = SimpleApp()
    editor = show_text_window.TextWindow(title=title, text_type='code', text=text)
    editor.resize(720, 450)
    editor.show()
    app.exec_()

    
def show_html(title="Title", text=""):
    '''Displays some html text in a window.

       :param title: the window title
       :param code: a string to display in the window.

       >>> import easygui_qt as easy
       >>> easy.show_html()

       .. image:: ../docs/images/show_html.png
    '''
    app = SimpleApp()
    editor = show_text_window.TextWindow(title=title, text_type='html', text=text)
    editor.resize(720, 450)
    editor.show()
    app.exec_()

    
def get_abort(message="Major problem - or at least we think there is one...",
              title="Major problem encountered!"):
    '''Displays a message about a problem.
       If the user clicks on "abort", sys.exit() is called and the
       program ends.  If the user clicks on "ignore", the program
       resumes its execution.

       :param title: the window title
       :param message: the message to display

       >>> import easygui_qt as easy
       >>> easy.get_abort()

       .. image:: ../docs/images/get_abort.png
    '''

    app = SimpleApp()
    reply = qt_widgets.QMessageBox.critical(None, title, message,
            qt_widgets.QMessageBox.Abort | qt_widgets.QMessageBox.Ignore)
    if reply == qt_widgets.QMessageBox.Abort:
        sys.exit()
    else:
        pass
    app.quit()

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

    get_abort(title=title, message=message)

def find_help():
    '''Opens a web browser, pointing at the documention about EasyGUI_Qt
       available on the web.
    '''
    webbrowser.open('http://easygui-qt.readthedocs.org/en/latest/api.html')


if __name__ == '__main__':
    try:
        from demos import guessing_game
        guessing_game.guessing_game()
    except ImportError:
        print("Could not find demo.")
