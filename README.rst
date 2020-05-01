=====
memon
=====

.. image:: https://travis-ci.org/TUW-GEO/memon.svg?branch=master
    :target: https://travis-ci.org/TUW-GEO/memon

.. image:: https://coveralls.io/repos/github/TUW-GEO/memon/badge.svg?branch=master
    :target: https://coveralls.io/github/TUW-GEO/memon?branch=master

.. image:: https://badge.fury.io/py/memon.svg
    :target: https://badge.fury.io/py/memon

.. image:: https://readthedocs.org/projects/memon/badge/?version=latest
    :target: http://memon.readthedocs.io/en/latest/?badge=latest

Very simple memory monitor that records the percent of memory used. This can be
useful if you want to dump data to disk if memory consumptions becomes too high.

Installation
============

This package should be installable through pip:

.. code::

    pip install memon

Description and Usage
=====================

The MemoryMonitor class takes an interval and a memory_limit in percent.

To start recording memory usage:

.. code::

    from memon import MemoryMonitor
    import time
    memmon = MemoryMonitor(interval=0.1)
    memmon.start()
    memmon.start_recording()
    time.sleep(1)
    memmon.stop_recording()
    assert len(memmon.history) == 10

If historical data is recorded this can be used to query if memory usage will
keep under the memory limit. This is done by calling:

.. code::

    memmon.memory_available()

This function makes some assumptions:

- The Python process is the main memory user on the system.
- Any big fluctuations in memory usage are because of memory
  allocation/deallocation of the process running the memon.
- We want to fit the average fluctuation that occurs during processing under the
  memory limit.

Because of these assumptions the ``memory_available()`` function calculates:

.. code::

   delta = max(history) - min(history)
   level = mean(history) + delta
   level < memory_limit

Contribute
==========

We are happy if you want to contribute. Please raise an issue explaining what
is missing or if you find a bug. We will also gladly accept pull requests
against our master branch for new features or bug fixes.

Development setup
-----------------

For Development we recommend a ``conda`` environment

Guidelines
----------

If you want to contribute please follow these steps:

- Fork the memon repository to your account
- make a new feature branch from the memon master branch
- Add your feature
- Please include tests for your contributions in one of the test directories.
  We use py.test so a simple function called test_my_feature is enough
- submit a pull request to our master branch

Note
====

This project has been set up using PyScaffold 3.2.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.
