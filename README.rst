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

  flake8 justic
  pylint --rcfile=setup.cfg justic

Create package::

  python -m pip install --upgrade twine
  python setup.py sdist bdist_wheel
  python -m twine check dist/*
  python -m twine upload dist/*
