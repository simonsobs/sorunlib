Configuration
=============

sorunlib tries to automatically determine as much about the OCS network as it
can, however some things still require configuration. This page details the
sorunlib configuration file.

.. note::
    This format is still under development and might change. Check back here if
    in doubt of formatting.

Example
-------

A full configuration file example with comments is shown here:

.. code-block:: yaml

    ---
    # sorunlib configuration

    # agents
    # sorunlib automatically detects unique agents on the OCS network, so only
    # non-unique agents need to be specified here.

    # ocs registry agent
    registry: 'registry'

Configuration Selection
-----------------------

Select the configuration file to load by setting the ``SORUNLIB_CONFIG``
environment variable:

.. code-block:: bash

    $ export SORUNLIB_CONFIG=/path/to/sorunlib/config.yaml

In practice, sorunlib is typically run within a Docker container, so it's quite
natural to set this in a compose file. The following example uses the
``so-daq-sequencer`` image:

.. code-block:: yaml

    sequencer-backend:
      image: ghcr.io/simonsobs/so-daq-sequencer:latest
      restart: always
      container_name: sequencer-backend
      environment:
        - OCS_CONFIG_DIR=/path/to/ocs/config/
        - SORUNLIB_CONFIG=/path/to/sorunlib/config.yaml
