Library Design
==============

This page describes the design goals of the library.

Overview
--------

sorunlib was designed with final script structure in mind. We are trying to
achieve something similar to the ACT script structure, except written in
Python. This should produce a human readable script that can easily be manually
manipulated when needed. During normal observations these scripts will be
automatically generated and run.

Library Structure
-----------------

The library splits the functions of different subsystems into different
modules. Here's an example layout from early development:

.. code-block::

    sorunlib
    ├── acu.py
    ├── commands.py
    ├── __init__.py
    ├── seq.py
    ├── smurf.py
    └── util.py

Functions that deal with only a single subsystem should be in their own module,
i.e. ``acu.py`` only deals with sending commands to the ACU. Functions that
coordinate multiple subsystems should go in ``seq.py`` (for 'sequence').

Example Script
--------------

An example script in sorunlib looks like:

.. code-block:: python

    from sorunlib import *
    
    initialize()
    
    wait("2022-02-16 18:00:00")
    acu.move_to(39.39, 64.27)
    smurf.iv_curve()
    wait("2022-02-16 18:05:00")
    smurf.bias_step()
    seq.scan("field")
    smurf.bias_step()


For comparison a similar ACT schedule looks like:

.. code-block::

    {soft_wait,{until,{2022,03,10},{20,00,00},utc}}
    {move_to,39.39,64.27}
    {mce,autotune,long}
    {mce,iv_curve}
    {soft_wait,{until,{2022,03,10},{20,06,05},utc}}
    {mce,bias_step}
    {scan,wide_01h_n,{until,{2022,03,10},{21,07,21},utc},32.90}
    {mce,bias_step}
