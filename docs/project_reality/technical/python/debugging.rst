
Debugging BF2 Python
====================

The BF2 engine includes debugging features, such as a log file that records useful information during gameplay. Python programs can write to this log file using the :py:meth:`host.log` method. Currently, how to enable this logging is unknown; it might be a command-line option. It's also possible that these debugging features were removed from the retail BF2 server, making the log non-existent.

The main DICE Python code has a debugging feature that sends its output to the BF2 engine log file using :py:meth:`host.log`. It does this by changing the ``stdout`` (standard output) and ``stderr`` (standard error message) streams. Instead of going to the console (which is mostly unavailable for the embedded Python interpreter), they are sent to :py:meth:`host.log`. There, they are recorded with other BF2 engine log information. After this change, a simple Python ``print`` statement will send its output to the log file.

The classes for this output redirection are in :py:mod:`bf2`. However, the redirection only starts when the BF2 engine calls :py:func:`bf2.init_module`. This means any ``print`` statements before this call will not produce output.

Near the beginning of the :py:mod:`bf2` module, you'll find the line ``g_debug = 0``. This :py:data:`bf2.g_debug` variable acts as a global flag (1 for active, 0 for inactive) that controls whether debugging information is printed across all BF2 Python modules. Throughout the DICE Python code, if there's information useful for debugging (like a 'we reached this point' message), the code checks :py:data:`bf2.g_debug`. If it's 1, the debugging information is printed. (To use :py:data:`bf2.g_debug` as a switch for your own modules, include ``from bf2 import g_debug`` in them).

So, what if :py:meth:`host.log` isn't working? You can redirect ``stdout`` and ``stderr`` to your own log file. Inside :py:func:`bf2.init_module` (in :file:`Battlefield 2 Server/python/_init_.py`, find the line "``def init_module():``"), look for this code:

.. code-block:: python

   sys.stdout = fake_stream('stdout')
   sys.stderr = fake_stream('stderr')

and replace it with:

.. code-block:: python

   logFile = open('mylogfile.log', 'a')
   sys.stdout = logFile
   sys.stderr = logFile

(The ``'a'`` means Python will "append" new output to the end of the log file, rather than overwriting it). This change will send all error messages and ``print`` statement outputs to :file:`Battlefield 2 Server/mylogfile.log`.

You can now use ``print`` statements in your Python code to get feedback on your program's activity.

Important Consideration
-----------------------

Due to how your operating system buffers input/output, you might not see anything in your log file until the ``stdout`` and ``stderr`` streams close or the operating system's buffer fills up. This could take a while, possibly not until the server shuts down. Even then, your output might disappear completely if the server doesn't shut down properly.

For instance, if you use the EA server GUI tool and click "Stop" while the server is running, it will shut down suddenly without saving its buffers, meaning your log file will be empty. To shut down the server gracefully, type "quit" directly into the server's window. If you have important information in the log file that you want to ensure is saved, use the ``sys.stdout.flush()`` method.

.. note::

   You can use :py:meth:`host.rcon_invoke` (e.g., ``host.rcon_invoke('echo "..."')``) to print things directly to the server console.
