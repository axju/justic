====================
justic - just static
====================
Let me explain what was inside my head as I start this:

There are a bunch of templates that defined some basic views, like a list-view,
a card-view or some grid-view. And the content files will be in another folder.
Every file contains some data and define the template for the render. The
structure of the files will be the structure of the output html files.

And there it is. **Still under development!**

Install
-------
.. code-block:: bash

  pip install justic

Example
-------
.. code-block:: bash

  python -m justic example
  python -m http.server --directory example/build


Content files
-------------
The content are simple python files with a specific structure. There are three
important sections:

JUSTIC (__JUSTIC__)
  For settings for the Justic class. This will be inherited to the sub
  directory.

META (__META__)
  Parameters for the current instance, like the template name or build file.

OTHERS
  All other capitalized variable will be passed to the template.

All Parameters:

.. code-block:: python

  __JUSTIC__ = {
    'remove_build_prefix': 'content',
    'default_template': 'index.html',
  }

  __META__ = {
    'target': 'content',
    'targets': ['content'],
    'static': 'static',
    'template': 'foo.html',
  }

  TITLE = 'Foo'
  SITEURL = ''

Development
-----------
Virtual environment windows::

  python -m venv venv
  venv\Scripts\activate

Virtual environment linux::

  python3 -m venv venv
  source venv/bin/activate

Setup project::

  python -m pip install --upgrade pip wheel setuptools coverage pytest flake8 pylint tox
  python -m pip install -e .

Run single test with code coverage::

  coverage run --source=justic -m pytest
  coverage report -m

Run test for multiple python versions::

  tox -p auto

Check syntax::

  python -m flake8 justic
  python -m pylint --rcfile=setup.cfg justic

Create package Jenkins will do it::

  git tag -a 0.1.7 -m "version 0.1.7"
  git push --follow-tags

No Jenkins?::

  python -m pip install --upgrade twine
  python setup.py sdist bdist_wheel
  python -m twine check dist/*
  python -m twine upload dist/*

ToDo
----

1. copy static don't work for sub directory
2. improve test
