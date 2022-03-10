========================
Contributing to sorunlib
========================

Style Guide
-----------

Contributors should follow the recommendations made in the `SO Developer
Guide`_. A brief summary is:

- Follow PEP08
- Use "Google Style" docstrings

.. _SO Developer Guide: https://simons1.princeton.edu/docs/so_dev_guide/

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
