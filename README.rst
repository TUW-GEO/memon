=====
memon
=====

Very simple memory monitor that records the percent of memory used. This can be
useful if you want to dump data to disk if memory consumptions becomes too high.

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

Note
====

This project has been set up using PyScaffold 2.5.7. For details and usage
information on PyScaffold see http://pyscaffold.readthedocs.org/.
