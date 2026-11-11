
Better Error Catching
=====================

:Original Author: King of Camelot

Problem
-------

Standard Python interpreters will stop execution when an unhandled exception (a programming error) occurs, and they will display a "traceback" message to help you identify the problem. However, the error handling built into the Python host embedded in Battlefield 2 only catches some errors, not all of them. When it fails to catch an error, the module where the problem occurred will usually stop running silently, while other modules continue to execute. This can make debugging very difficult for programmers, as troubleshooting bad code without error messages is challenging, and adding ``print`` statements everywhere to pinpoint failures is far from ideal.

Solution
--------

Python offers ``Try`` statements that allow you to catch and display errors that would otherwise go unnoticed. Specifically, we will use the ``Try...Except`` statement, which consists of two parts. The first part, the ``Try`` block, is where you place the code you want to execute. The second part, the ``Except`` block, contains the code that will run if an exception (error) occurs. A simple example looks like this:

.. code-block:: python

   Try:
      # Place the code you want to execute here
   Except:
      # Place the code that should run if an error occurs here

In this example, I use a general ``Except`` block, which will catch all exceptions. You can specify particular types of errors if you know what kind of exception might occur in your code, such as ``Except ImportError``. For a list of specific exceptions, refer to: `Python Exceptions <https://docs.python.org/release/2.3.4/lib/module-exceptions.html>`_.

Next, let's look at the code we want to execute when an exception happens. When an exception occurs, three different values are stored in ``sys.exc_info()``. The first value is the type of exception, the second provides specific details about the exception, and the third gives you a reference to a traceback object for that exception. This makes it easy to get detailed information about an exception when it occurs. In the following example, I also use functions from both the `Inspect Module <https://docs.python.org/release/2.3.4/lib/module-inspect.html>`_ (to get the source code file name) and the `Re Module <https://docs.python.org/release/2.3.4/lib/module-re.html>`_ (to format strings):

.. code-block:: python

   import inspect
   import re

   def ExceptionOutput():
      sys.stderr.write("\n" + "Exception Occurred: " + str(sys.exc_info()[0]) + "\n")
      sys.stderr.write("Value: " + str(sys.exc_info()[1]) + "\n")
      sys.stderr.write("Line:" + str(readline(inspect.getfile(sys.exc_info()[2]),
                        sys.exc_info()[2].tb_lineno)) + "\n")
      sys.stderr.write("Line #: " + str(sys.exc_info()[2].tb_lineno) + "\n")
      sys.stderr.write("File: " + str(inspect.getfile(sys.exc_info()[2])) + "\n" + "\n")

   def readline(filename, lineno):
      filen = re.sub('\\\\', '/', filename)
      file = open(filen, 'rU')
      lines = file.readlines()
      file.close()
      linen = lineno - 1
      line = re.sub('\s+', ' ', lines[linen])
      return line

Let's explain the two functions we've just defined:

- The function ``readline`` takes two arguments: a file name and a line number.

  - The file name is obtained using ``inspect.getfile(object)``, which takes an object and returns the name of the source code file it originated from.
  - The line number is obtained using ``object.tb_lineno``. The "tb" in ``tb_lineno`` refers to a traceback object.
  - In both cases above, the object is the third value stored in ``sys.exc_info()``.
  - Moving to the core of the function, the first line formats the file name argument by converting all backslashes to forward slashes. The reason for this will be explained shortly.
  - The next line opens the file specified by the newly formatted file name. The file name needed to be formatted first because, although ``inspect.getfile(object)`` returns a name with backslashes, the ``open`` method requires a file name with forward slashes.
  - With the source code file now open, we extract all its lines using ``file.readlines()``.
  - We then close the file, as we are finished with it.
  - We subtract one from the line number because, while source code file line numbers typically start from 1 (1, 2, 3...), the list (or array) where the lines are stored is zero-indexed (0, 1, 2, 3...).
  - Normally, the returned line would have a lot of extra whitespace at the beginning due to Python's use of whitespace in its source code files. Since this doesn't look good in an error log, we use a substitution function to remove all the excess whitespace.
  - Finally, the function returns the source code line corresponding to the input line number.

- The function ``ExceptionOutput`` takes no arguments, but it generates a clear error message for us.

  - The first line outputs the first value in ``sys.exc_info()``, which is the type of exception.
  - The next line outputs the second value of ``sys.exc_info()``, which provides specific details about the exception.
  - Next, we output the source code line where the exception occurred, using the ``readline`` function.
  - To make it easier to locate, we also output the line number where the exception occurred.
  - The last piece of information we output is the name of the source code file where the exception occurred.

Now, let's look at an example of how to implement these functions:

.. code-block:: python

   def onEnterVehicle(player, vehicle, freeSoldier = False):
      try:
         print "Entered: ", vehicle.templateName
         print vehicle.getDamage()
         print vehicle.hasArmor
         print vehicle.getName()
      except:
         ExceptionOutput()

In this example, an error would occur at ``print vehicle.getName()``, and we would receive a clear error message from ``ExceptionOutput()``. The ``Try...Except`` statement stops processing code within the ``try`` section as soon as an exception occurs. This means that even if there are multiple exceptions within the ``try`` block, you will only see the first one that Python encounters. Once you fix that exception and re-execute your code, it should continue and catch any other errors present in your code.

Discussion
----------

When I originally wrote this code, I was specifically working with the `BF2 Python Log <http://wikihost.org/wikis/bf2modding/>`_. The code should also work with other logging systems, but it might require minor adjustments. I recommend using the `BF2 Python Log <http://wikihost.org/wikis/bf2modding/>`_ because it allows you to see errors in real-time, and the error messages are displayed in clear red text.

Please remember that this is just one example, and there are other ways to achieve similar results. For instance, in my code, I used one large ``Try...Except`` statement that enclosed all the code within the ``try`` section. You could divide it into several smaller ``Try...Except`` statements, with only a small amount of code in each. This can be useful for being more specific about the type of exception you want to catch. You could also use a ``Try...Except...Else`` statement. In a ``Try...Except...Else`` statement, the ``else`` section executes only if no exception occurs in the ``try`` section, but no exception checking happens within the ``else`` section itself. More information on ``try`` statements can be found here: `Try Statements <https://docs.python.org/release/2.3.4/ref/try.html>`_.
