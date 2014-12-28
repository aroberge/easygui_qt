"""EasyGUI_Qt: procedural gui based on PyQt

EasyGUI_Qt is inspired by EasyGUI and contains a number
of different basic graphical user interface components
"""

import os
import sys
import collections
import functools
import inspect
if sys.version_info < (3,):
    import ConfigParser as configparser
else:
    import configparser
    unicode = str

from PyQt4 import QtGui, QtCore

__all__ = [
    'show_message',
    'get_choice',
    'get_list_of_choices',
    'get_float',
    'get_int',
    'get_integer',
    'get_string',
    'get_yes_or_no',
    'get_directory_name',
    'get_file_names',
    'get_save_file_name',
    'set_font_size',
    'select_language',
    'set_language',
]

QM_FILES = None

def with_app(func):
    """Intended to be used as a decorator to ensure that a single app
       is running before the function is called, and stopped afterwords
    """

    def _decorator(*args, **kwargs):
        """A single decorator would be enough to start an app before the
           function is called. By using an inner decorator, we can quit
           the app after the function is done.
        """
        app = SimpleApp()
        kwargs['app'] = app
        try:
            response = func(*args, **kwargs)
        except TypeError:  # perhaps 'app' was not a keyword argument for func
            if sys.version_info < (3, 3):  # assume it was the problem
                del kwargs['app']
                response = func(*args, **kwargs)
            else:
                sig = inspect.signature(func)  # sig did not exist before 3.3
                if 'app' in sig.parameters.values():
                    raise
                else:
                    del kwargs['app']
                    response = func(*args, **kwargs)
        app.quit()
        return response

    return functools.wraps(func)(_decorator)


def find_qm_files():
    """looking for files with names == qt_locale.qm"""
    all_files = collections.OrderedDict()
    for root, _, files in os.walk(os.path.join(QtGui.__file__, "..")):
        for fname in files:
            if (fname.endswith('.qm') and fname.startswith("qt_")
                    and not fname.startswith("qt_help")):
                locale = fname[3:-3]
                all_files[locale] = root
    return all_files


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
            QM_FILES = find_qm_files()
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


class _LanguageSelector(QtGui.QDialog):
    """A specially constructed dialog which uses informations about
       available language (qm) files which can be used to change the
       default language of the basic PyQt ui components.
    """

    def __init__(self, parent, title="Language selection",
                 name="Language codes",
                 instruction="Click button when you are done"):
        super(_LanguageSelector, self).__init__(None,
                         QtCore.Qt.WindowSystemMenuHint |
                         QtCore.Qt.WindowTitleHint)

        self.qm_files_choices = {}
        self.parent = parent

        # ========= check boxes ==============
        group_box = QtGui.QGroupBox(name)
        group_box_layout = QtGui.QGridLayout()
        for i, locale in enumerate(QM_FILES):
            check_box = QtGui.QCheckBox(locale)
            check_box.setAutoExclusive(True)
            self.qm_files_choices[check_box] = locale
            check_box.toggled.connect(self.check_box_toggled)
            group_box_layout.addWidget(check_box, i / 4, i % 4)
        # adding default language option. When using the PyQt distribution
        # no "en" files were found and yet "en" was the obvious default.
        # We need this option in case we want to revert a change.
        check_box = QtGui.QCheckBox("Default")
        check_box.setAutoExclusive(True)
        self.qm_files_choices[check_box] = "default"
        check_box.toggled.connect(self.check_box_toggled)
        i = len(QM_FILES)
        group_box_layout.addWidget(check_box, i / 4, i % 4)
        group_box.setLayout(group_box_layout)

        # ========= buttons ==============
        button_box = QtGui.QDialogButtonBox()
        confirm_button = button_box.addButton(QtGui.QDialogButtonBox.Ok)
        confirm_button.clicked.connect(self.confirm)

        # ========= finalizing layout ====
        main_layout = QtGui.QVBoxLayout()
        main_layout.addWidget(group_box)
        main_layout.addWidget(QtGui.QLabel(instruction))
        main_layout.addWidget(button_box)
        self.setLayout(main_layout)
        self.setWindowTitle(title)

    def check_box_toggled(self):
        """Callback when a checkbox is toggled"""
        self.locale = self.qm_files_choices[self.sender()]

    def confirm(self):
        """Callback from confirm_button used to set the locale"""
        if self.locale != self.parent.config['locale']:
            self.parent.set_locale(self.locale)
            print(self.locale)
        self.close()


class MultipleChoicesDialog(QtGui.QDialog):
    """Dialog with the possibility of selecting one or more
       items from a list"""
    def __init__(self, choices=None, title="Title"):
        super(MultipleChoicesDialog, self).__init__(None, QtCore.Qt.WindowSystemMenuHint |
                         QtCore.Qt.WindowTitleHint)
        if choices is None:
            choices = ["Item %d"%i for i in range(10)]
        self.setWindowTitle(title)
        self.selection = []

        main_widget = QtGui.QWidget()
        main_layout = QtGui.QVBoxLayout()
        main_widget.setLayout(main_layout)

        self.choices_widget = QtGui.QListWidget()
        self.choices_widget.setSelectionMode(
                                    QtGui.QAbstractItemView.ExtendedSelection)
        for choice in choices:
            item = QtGui.QListWidgetItem()
            item.setText(choice)
            self.choices_widget.addItem(item)
        main_layout.addWidget(self.choices_widget)

        button_box_layout = QtGui.QGridLayout()
        selection_completed_btn = QtGui.QPushButton("Ok")
        selection_completed_btn.clicked.connect(self.selection_completed)
        select_all_btn = QtGui.QPushButton("Select all")
        select_all_btn.clicked.connect(self.select_all)
        clear_all_btn = QtGui.QPushButton("Clear all")
        clear_all_btn.clicked.connect(self.clear_all)
        cancel_btn = QtGui.QPushButton("Cancel")
        cancel_btn.clicked.connect(self.cancel)

        button_box = QtGui.QWidget()
        button_box_layout.addWidget(select_all_btn, 0, 0)
        button_box_layout.addWidget(clear_all_btn, 1, 0)
        button_box_layout.addWidget(cancel_btn, 0, 1)
        button_box_layout.addWidget(selection_completed_btn, 1, 1)
        button_box.setLayout(button_box_layout)

        main_layout.addWidget(button_box)
        self.setLayout(main_layout)
        self.show()

    def selection_completed(self):
        """Selection completed, set the value and close"""
        self.selection = [item.text() for item in
                          self.choices_widget.selectedItems()]
        self.close()

    def select_all(self):
        """Set all possible values as selected"""
        self.choices_widget.selectAll()
        self.selection = [item.text() for item in
                          self.choices_widget.selectedItems()]

    def clear_all(self):
        """Reset to have no selected values"""
        self.choices_widget.clearSelection()
        self.selection = []

    def cancel(self):
        """cancel and set the selection to an empty list"""
        self.selection = []
        self.close()


@with_app
def get_yes_or_no(question="Answer this question", title="Title"):
    """Simple yes or no question.

       :param question: Question (string) asked
       :param title: Window title (string)

       :return: ``True`` for "Yes", ``False`` for "No",
               and ``None`` for "Cancel".

       >>> import easygui_qt as easy
       >>> easy.get_yes_or_no()

       .. image:: ../docs/images/yes_no_question.png
    """
    flags = QtGui.QMessageBox.Yes | QtGui.QMessageBox.No
    flags |= QtGui.QMessageBox.Cancel

    reply = QtGui.QMessageBox.question(None, title, question, flags)
    if reply == QtGui.QMessageBox.Yes:
        return True
    elif reply == QtGui.QMessageBox.No:
        return False


@with_app
def select_language(title="Select language", name="Language codes",
                    instruction=None, app=None):
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
    if instruction is None:
        instruction = ('Current language code is "{}".'.format(
                                                        app.config['locale']))
    selector = _LanguageSelector(app, title=title, name=name,
                                 instruction=instruction)
    selector.exec_()


@with_app
def set_language(locale, app=None):
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
    app.set_locale(locale)


@with_app
def show_message(message="Message", title="Title"):
    """Simple message box.

       :param message: message string
       :param title: window title

       >>> import easygui_qt as easy
       >>> easy.show_message()

       .. image:: ../docs/images/show_message.png
    """
    box = QtGui.QMessageBox(None)
    box.setWindowTitle(title)
    box.setText(message)
    box.show()
    box.exec_()


@with_app
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
    flags = QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint
    number, ok = QtGui.QInputDialog.getInteger(None,
                                               title, message,
                                               default_value, min_, max_, step,
                                               flags)
    if ok:
        return number
get_integer = get_int


@with_app
def get_float(message="Choose a number", title="Title",
                  default_value=0., min_=-10000, max_=10000, decimals=3):
    """Simple dialog to ask a user to select a floating point number
       within a certain range and a maximum precision.

       :param message: Message displayed to the user, inviting a response
       :param title: Window title
       :param default_value: Default value for integer appearing in the text
                             box; set to the closest of ``min_`` or ``max_``
                             if outside of allowed range.
       :param min_: Minimum integer value allowed
       :param max_: Maximum integer value allowed
       :param decimals: Indicate the maximum decimal precision allowed

       :return: an integer, or ``None`` if "cancel" is clicked or window
                is closed.

       >>> import easygui_qt as easy
       >>> number = easy.get_float()

       .. image:: ../docs/images/get_float.png
    """
    flags = QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint
    number, ok = QtGui.QInputDialog.getDouble(None,
                                              title, message,
                                              default_value, min_, max_,
                                              decimals, flags)
    if ok:
        return number

@with_app
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
    flags = QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint
    text, ok = QtGui.QInputDialog.getText(None, title, message,
                                          QtGui.QLineEdit.Normal,
                                          default_response, flags)
    if ok:
        if sys.version_info < (3,):
            return unicode(text)
        return text

@with_app
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
    flags = QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint
    choice, ok = QtGui.QInputDialog.getItem(None, title,
            message, choices, 0, False, flags)
    if ok:
        if sys.version_info < (3,):
            return unicode(choice)
        return choice


@with_app
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
    dialog = MultipleChoicesDialog(title=title, choices=choices)
    dialog.exec_()
    if sys.version_info < (3,):
        return [unicode(item) for item in dialog.selection]
    return dialog.selection


@with_app
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
    options = QtGui.QFileDialog.Options()
    # Without the following option (i.e. using native dialogs),
    # calling this function twice in a row made Python crash.
    options |= QtGui.QFileDialog.DontUseNativeDialog
    options |= QtGui.QFileDialog.DontResolveSymlinks
    options |= QtGui.QFileDialog.ShowDirsOnly
    directory = QtGui.QFileDialog.getExistingDirectory(None,
                                            title, os.getcwd(), options)
    if sys.version_info < (3,):
        return unicode(directory)
    return directory


@with_app
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

    if sys.version_info < (3,):
        files = QtGui.QFileDialog.getOpenFileNames(None, title, os.getcwd(),
                                               "All Files (*.*)")
        files = [unicode(item) for item in files]
    else:
        options = QtGui.QFileDialog.Options()
        options |= QtGui.QFileDialog.DontUseNativeDialog
        files = QtGui.QFileDialog.getOpenFileNames(None, title, os.getcwd(),
                                               "All Files (*.*)", options)
    return files


@with_app
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

    if sys.version_info < (3,):
        file_name = QtGui.QFileDialog.getSaveFileName(None, title, os.getcwd(),
                                               "All Files (*.*)")
        return unicode(file_name)

    options = QtGui.QFileDialog.Options()
    options |= QtGui.QFileDialog.DontUseNativeDialog  # see get_directory_name
    file_name = QtGui.QFileDialog.getSaveFileName(None, title, os.getcwd(),
                                               "All Files (*.*)", options)
    return file_name

@with_app
def set_font_size(font_size, app=None):
    """Simple method to set font size.

    :param font_size: integer value

    Does not create a GUI widget; but affects the appearance of
    future GUI widgets.

    >>> import easygui_qt as easy
    >>> easy.set_font_size(20)
    >>> easy.show_message()

    .. image:: ../docs/images/set_font_size.png
    """
    app.set_font_size(font_size)

if __name__ == '__main__':
    try:
        from demos import guessing_game
        guessing_game.guessing_game()
    except ImportError:
        print("Could not find demo.")
