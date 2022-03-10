========
sorunlib
========

.. image:: https://img.shields.io/github/workflow/status/simonsobs/sorunlib/Run%20Tests
    :target: https://github.com/simonsobs/sorunlib/actions?query=workflow%3A%22Run+Tests%22
    :alt: GitHub Workflow Status

.. image:: https://readthedocs.org/projects/sorunlib/badge/?version=latest
    :target: https://sorunlib.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://coveralls.io/repos/github/simonsobs/sorunlib/badge.svg?branch=main
    :target: https://coveralls.io/github/simonsobs/sorunlib?branch=main

Overview
--------

A high level library for running observatory operations. `sorunlib` handles
connecting to running OCS Agents and sending the appropriate commands for
running commands for a single telescope platform.

Installation
------------

Clone this repository and install using pip::

    $ git clone https://github.com/simonsobs/sorunlib.git
    $ cd sorunlib
    $ pip install .

Install optional dependencies with::

    $ pip install .[tests]
    $ pip install .[docs]
    $ pip install .[tests,docs]

Documentation
-------------

The sorunlib documentation can be built using Sphinx. Be sure to install the
optional "docs" dependencies when installing above. Then run::

  $ cd docs/
  $ make html

You can then open ``docs/_build/html/index.html`` in your preferred web
browser. You can also find a copy hosted on `Read the Docs`_.

.. _Read the Docs: https://sorunlib.readthedocs.io/en/latest/

Tests
-----

The tests can be run using pytest, and should be run from the ``tests/``
directory::

    $ cd tests/
    $ python3 -m pytest

License
-------

This project is licensed under the BSD 2-Clause License - see the
`LICENSE.txt`_ file for details.

.. _LICENSE.txt: https://github.com/simonsobs/sorunlib/blob/main/LICENSE.txt
