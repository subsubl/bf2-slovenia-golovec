
Adding New RCon Commands
========================

:Original Author: Woody

Problem
-------

You want to create your own RCon command(s) to add administrative features to BF2. However, you prefer not to modify the standard BF2 administration module's code, as you understand that altering standard code is generally not recommended.

Solution
--------

Utilize the dynamic object modification technique explained in :doc:`this recipe <changing_objects>`. Simply import the following function from one of the main modules:

.. py:function:: registerRConCommand(command, function)

   This function registers a custom RCon command by dynamically adding a function that implements the new command as a new method of the ``default.AdminServer`` class.

   :param str command: The name of the new RCon command.
   :param function: The Python function that implements the command's logic.

   .. code-block:: python

      import new, default

      def registerRConCommand(command, function):
         # Embed the function into a new instancemethod object, bound to the AdminServer
         newMethod = new.instancemethod(function, default.server, default.AdminServer)

         # Create a new class attribute in AdminServer, linking it to our function
         setattr(default.AdminServer, command, newMethod)

         # Add the new command to the rcon dispatch table, pointing to our function
         default.server.rcon_cmds[command] = newMethod

:py:func:`registerRConCommand` handles all the necessary steps to create a new RCon command. To use it, you only need to define the Python function that your new RCon command should execute, and then call :py:func:`registerRConCommand` to register your new command and link it to your function:

.. code-block:: python

   '''
   Create a function that executes our desired new RCon command. Note that since this will be a method within a class, the first argument to the function MUST be "self", even if it's not explicitly used. The admin module also passes "ctx" (command context) and "cmd" (the remainder of the RCon command line) to our function.
   '''

   def rcmd_mycmd(self, ctx, cmd):
      # You can make your new command perform any desired action here
      ctx.write("We're now executing mycmd.\n")

   # Now, register the new RCon command
   registerRConCommand('mycmd', rcmd_mycmd)

Once this code is imported, your new RCon command will be active. After you authenticate (using ``rcon login``), you can execute your command from the server console or an in-game player console by typing ``rcon mycmd``.

If you wish to execute it from an RCon TCP connection, you simply need to type ``mycmd`` (without the "rcon" prefix).

Discussion
----------

You can add as many commands as you want, and each can implement any function you desire. These commands will behave exactly as if they were originally coded in the :file:`Battlefield 2 Server/admin/default.py` file, even though you never had to modify that file!

This approach is incredibly useful because directly modifying standard files makes it very difficult to upgrade to new versions of BF2 later. Furthermore, if you have multiple mods or add-ons that all try to add their own RCon commands by modifying the original code, they will quickly conflict and break each other. This dynamic approach is much cleaner. In fact, you can have multiple scripts like this, developed separately by different people, and when they are imported, they will work together seamlessly without issues (unless two developers choose identical names for their new commands).
