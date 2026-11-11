
The Administrative Module
=========================

Battlefield 2 includes a Python "administrative" module. This module is highly versatile, but the Python code provided with BF2 primarily serves two functions:

#. It implements the BF2 RCon ("Remote Console") interface.
#. It handles several automatic in-game administration tasks. The standard module automatically balances player numbers on each team and manages penalties for players who kill teammates ("TK"ing).

The ``sv.adminScript`` server configuration directive tells the BF2 game engine which administrative module to load during startup. This directive specifies the name of the Python module located in the ``Battlefield 2 Server/admin`` directory. The default administrative module included with BF2 is, appropriately, named ``default``:

.. code-block:: python

   sv.adminScript "default"

You can create your own administrative modules. Simply place them in the ``Battlefield 2 Server/admin`` directory and update the ``sv.adminScript`` setting in the :file:`ServerSettings.con` file.

Module Methods
--------------

Any administrative module, including the ``default`` module, contains three methods that are automatically called by the game engine:

``init()``
   The game engine calls this method during its :doc:`startup process <../python/big_picture>`. In the ``default`` module, this method reads the admin configuration file (:file:`default.cfg`), sets up the admin system, and registers to receive :doc:`RemoteCommand events <../python/reference/events>`, among other tasks.

``shutdown()``
   The game engine calls this method when the server is completely shutting down (not just after each game round). In the ``default`` module, this method simply closes the TCP socket used for receiving RCon commands from the network.

``update()``
   The game engine calls this method approximately every 30 milliseconds. In the ``default`` module, this method checks for any new input arriving via the network TCP RCon socket.

RCon
----

BF2 includes an ``RCon`` (Remote Console) feature that allows many administrative tasks, typically performed from the standard console (the black-and-white curses interface on the BF2 server machine), to be executed from a "remote console." This can be done either from within a BF2 game client (by a player pressing the ``~`` key) or through a TCP network interface.

The ``RCon`` interface is entirely implemented in Python, with its code located in the ``Battlefield 2 Server/admin`` directory. The game engine provides five mechanisms that this Python code utilizes:

- As part of its :doc:`startup procedure <../python/big_picture>`, the server imports the Python module specified by the ``sv.adminScript`` directive in the ``admin`` directory. This is typically the ``default`` module, but because it's imported based on a configuration directive, it can easily be swapped for a custom module.
- The game engine offers a :doc:`RemoteCommand <../python/reference/events>` event. This event triggers whenever an in-game player accesses their console and types a line that begins with "rcon". The event then passes the actual command typed by the player to any registered callback handlers. This is how the ``default`` module receives ``RCon`` commands from players (though other Python code can also use this).
- The game engine provides a method, ``host.rcon_feedback``, which can be used to send messages to a player's in-game console. The ``default`` module uses this to send responses to players' ``RCon`` commands back to them (and other Python code can use it too).
- The game engine repeatedly calls the ``update`` method of the ``default`` module (or whichever module is specified by ``sv.adminScript``), generally about every 30 milliseconds (approximately 30 times per second). The ``default`` module uses this to quickly check for incoming ``RCon`` commands on a TCP port (usually port 4711). This is how the network ``RCon`` interface receives commands. More details about the ``RCon`` protocol implemented by the ``default`` module can be found in the :doc:`RCon Protocol Specification <../networking/protocols_rcon>`.
- When the ``default`` module decides to execute a console command from a remote user, it forwards the command to the game engine for execution using the ``host.rcon_invoke`` method. This method is not specific to ``RCon`` commands; in fact, it doesn't execute ``RCon`` commands at all. Instead, it executes server console commands and can be effectively used by any Python code. However, there is currently a bug in BF2 that prevents any feedback from PunkBuster commands from being sent back to the caller of ``host.rcon_invoke``. Since this is the only way remote console commands are executed, it means that ``RCon`` users will never see feedback from PunkBuster commands they send via ``RCon``.

The ``default`` module includes only three RCon commands (but can be easily expanded to include more):

``login``
   The ``default`` module will not accept any other RCon commands until this command is provided with the correct password, as defined in the :file:`default.cfg` file.

``users``
   This command lists players currently connected to the server, along with their :doc:`IP Addresses and CD key hashes <identity>`.

``exec``
   This command executes any server command.

.. note::

   When using a player's in-game console window, each of these commands must be preceded by the word "rcon" to ensure the game engine sends it to the ``default`` module. When connecting via TCP RCon, these commands should be typed exactly as shown.

Other Administrative Functions
------------------------------

When the game engine loads the ``default`` administrative module, one of its actions is to import the ``standard_admin`` module. Upon being imported, ``standard_admin`` then imports and initializes two additional modules:

- ``standard_admin.autobalance``
- ``standard_admin.tk_punish``
