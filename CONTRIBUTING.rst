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

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "feature"
is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

easygui_qt, like any project, could always use more documentation, whether as part of the
official easygui_qt docs, in docstrings, or even on the web in blog posts,
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
   Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    $ mkvirtualenv easygui_qt
    $ cd easygui_qt/
    $ python setup.py develop

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. Make sure you check your code, running any tests or demos, and see that it
   follows PEP8

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

IMPORTANT: I actually have
never used git for a pull request; in all previous projects, I always
did a diff of the proposed code (usually submitted as a patch or
comparing actual submitted files using a diff program) and carefully
reviewed suggested changes before incorporating them "by hand".


Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests - or possibly some working demos
   as this might be more useful given the visual nature of this project.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.  Or not.
3. The pull request should work for at least Python 3.3, and 3.4.

Tips
----

(Not true yet!)

To run a subset of tests::

    $ python -m unittest tests.test_easygui_qt
