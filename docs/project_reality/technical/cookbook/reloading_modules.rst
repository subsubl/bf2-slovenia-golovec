
Reloading Modules at Runtime
============================

:Original Author: King of Camelot

Problem
-------

Are you tired of restarting the server every time you modify your Python code? Simple changes that should take only a few seconds often turn into minutes because you have to shut down and restart the server just to see the effects of your coding.

Solution
--------

Python's nature as a `dynamic language <https://en.wikipedia.org/wiki/Dynamic_language>`_ allows us to reload a module while the main Python code is still running. To achieve this, I've divided the process into two parts: first, a header file to set up the reload function and other necessary components, and then the module where your actual code resides.

The Header File
---------------

The header file will contain the function code responsible for reloading your module. Unfortunately, Battlefield 2 allows you to register for events in your code but does not provide a way to unregister them. This creates a problem: even after reloading a module, the old code registered to an event will still execute when that event fires. This results in both your old and new code running simultaneously, which is far from ideal. To work around this, I decided to set up the events in the header file under different names. Then, when an event fires, the code in the header file will call your code (using its normal name) within your module. The commented code below illustrates this:

.. code-block:: python

   import host
   import sys
   import bf2.mymodule
   import inspect
   import re

   def init():
      # Configure any events you will use in your code.
      # These can be modified later, but only if you restart the server.
      # Note the '_Header' suffix added to the end of the event names.
      # This suffix is essential for correct functionality.

      host.registerHandler('EnterVehicle', onEnterVehicle_Header)
      host.registerHandler('ExitVehicle', onExitVehicle_Header)

      # This event will be used by the header to determine when to reload the module.
      # If you intend to use the ChatMessage event in your own code, I suggest you
      # register it above like the others and leave this as is.

      host.registerHandler('ChatMessage', onChatMessage)

   def onEnterVehicle_Header(player, vehicle, freeSoldier = False):
      # This event acts as a wrapper, receiving information
      # and then forwarding it to the module.

      bf2.mymodule.onEnterVehicle(player, vehicle, freeSoldier = False)

   def onExitVehicle_Header(player, vehicle):
      # This event acts as a wrapper, receiving information
      # and then forwarding it to the module.

      bf2.mymodule.onExitVehicle(player, vehicle)

   def onChatMessage(playerId, text, channel, flags):
      # This is a fairly simple usage example.
      # It checks chat messages for the word 'reset'.
      # When found, it reloads your module.
      # For this to work as intended, use 'Say All:'.

      if text == 'reset':
         try:
            reload(bf2.mymodule)
         except:
            sys.stderr.write("\n" + "Couldn't reload module, an exception occurred")
            ExceptionOutput()

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

.. note::

   After writing my cookbook recipe on better error catching, I decided to update the reload function to display an error message if an error occurs during loading. (I encountered several such errors while developing the error catching recipe, and they were quite frustrating. Yes, I recognize the irony of encountering errors while working on better error handling.) If the reload fails, your old code will continue to execute until a successful reload occurs. For more details on the implemented error catching, :doc:`click here <error_catching>`.

The Module File
---------------

Next is the actual module where you will place your custom code. From a coding perspective, nothing has fundamentally changed. The only difference is that instead of registering for event callbacks directly in your module, you now do so in the header file. Otherwise, all imports, functions, and other elements should work correctly within your module. For simplicity, here is an example module named :file:`mymodule.py`:

.. code-block:: python

   # Set up any imports you need for your module

   def onEnterVehicle(player, vehicle, freeSoldier = False):
      # Configure your events as you normally would.
      # For this example, I will use a simple print command
      # to demonstrate its functionality.
      print "Entered:", vehicle.templateName

   def onExitVehicle(player, vehicle):
      # Configure your events as you normally would.
      # For this example, I will use a simple print command
      # to demonstrate its functionality.
      print "Exited:", vehicle.templateName

Discussion
----------

Reloading files at runtime can save a significant amount of time. All you need to do is minimize the game, modify and save your module, then reopen the game and type 'reset' in the public chat. I separated this into a header and module file, but it might be possible to combine them into a single file. I found this approach simpler, as it allows you to link multiple modules to the same header file, reducing redundant code. Additionally, I chose to use a chat message as the trigger for a reload for simplicity; however, you could configure it to work with any event you prefer.

This was a learning experience for me, so there might be some inaccuracies. Please feel free to point out any errors or suggest improvements. Remember, these are just examples to help you understand the concept of reloading files; there are several other ways this could be implemented.
