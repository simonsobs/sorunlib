========================
Contributing to sorunlib
========================

Development
-----------

For development you should install sorunlib from source (choice of environment
is left to the reader)::

    $ git clone https://github.com/simonsobs/sorunlib.git
    $ cd sorunlib
    $ pip install -e .[tests,docs]

This will install an editable version with the optional dependencies for
testing and building the docs.

Style Guide
-----------

Contributors should follow the recommendations made in the `SO Developer
Guide`_. A brief summary is:

- Follow PEP08
- Use "Google Style" docstrings

.. _SO Developer Guide: https://simons1.princeton.edu/docs/so_dev_guide/

pre-commit
``````````

To help with styling we use pre-commit. You can install the pre-commit hooks
with::

    $ pip install pre-commit
    $ pre-commit install

This will then run flake8 on editted files before committing.

Branches + PRs
--------------

``main`` is the only long-lived branch. Please create feature branches and PR
onto ``main``.

Tests
-----

This library is critical to running observations at the site. While we will be
testing sorunlib in the labs, please include unit tests with your PRs, or
explicitly exclude code from coverage if there is good reason that it should
not be tested.
