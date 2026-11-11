
Time in BF2
===========

Battlefield 2 primarily measures time using "wall time"—the high-resolution seconds elapsed since the server started (e.g., ``443.451488108``). Unlike *Battlefield: 1942* and *Battlefield: Vietnam* servers, the BF2 server doesn't restart between rounds, so wall time keeps increasing.

.. code-block:: python
   :caption: You can get the current wall time like this:

   timeNow = host.timer_getWallTime()

Most (possibly all) time measurements in BF2 are in seconds and based on wall time.

.. code-block:: python
   :caption: Other time functions are available:

   import time

   # Gets current epoch time (seconds since January 1, 1970)
   epochTime = time.time()
   # Or, to get a formatted, user-friendly date and time string
   dateString = time.strftime("%m-%d-%y %H:%M")

See the `Python Library Reference <https://docs.python.org/release/2.3.4/lib/module-time.html>`_ for more information about ways to manipulate dates and times in Python.
