============
Contributing
============

The following has been adapted from the boilerplate version created by cookiecutter.
*Make sure you read the relevant parts as I do things a bit differently.* ;-)


Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/aroberge/easygui_qt/issues.

If you are reporting a bug, please include:

* Have a look first at the existing issues (even the closed ones) - to avoid duplication.
* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.
* Screen captures can be useful.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "feature"
is open to whoever wants to implement it.
You might want to have a look at
https://github.com/aroberge/easygui_qt/issues/13

Something that would be **really nice** is to have unittest working that
make use of QTest.  I just have not been able to do this.  I started
implementing unittests using pyautogui but it (like Sikuli which could
be another alternative) requires the windows to be left on their own while
the tests are "slowly" executed; furthermore, it had been found to be
unreliable on OSX with Python 2.7 (no report about OSX + Python 3+) as
the windows appear "under" other already present.

Write Documentation
~~~~~~~~~~~~~~~~~~~

EasyGUI_Qt, like any project, could always use more documentation,
whether as part of theofficial EasyGUI_Qt docs, in docstrings,
or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at
https://github.com/aroberge/easygui_qt/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Try to provide a specific use-case. Please note that some good ideas may
  not be implemented so as to keep the API easy to use for beginners.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `easygui_qt` for local development.

1. Fork the `easygui_qt` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/easygui_qt.git

3. Install your local copy into a virtualenv.
   Assuming you have virtualenvwrapper installed, this is how you set
   up your fork for local development::

    $ mkvirtualenv easygui_qt
    $ cd easygui_qt/
    $ python setup.py develop

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. Make sure you check your code, running any tests or demos, and see that it
   follows PEP8.  If you are adding a new widget, add it to the launcher
   demo.

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------


Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests ... well, if I get tests working
   properly.  If it is a new widget, you should add it to the launcher
   and possibly creating a specific demo.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring.
3. The pull request should work for at least Python 3.3, and 3.4. ...
   Ideally, it should also be tested with Python 3.2 and Python 2.7 as it
   would be nice to support these older version.


