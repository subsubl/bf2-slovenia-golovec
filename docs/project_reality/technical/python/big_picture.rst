
How BF2 Hooks Python
====================

This describes how the BF2 engine uses Python code:

#. When BF2 engine starts up it fires up its embedded Python interpreter, with it's ``sys.path`` set to include:

   - The Python standard library

      Contained in the file :file:`Battlefield 2 Server/pylib-2.3.4.zip`

   - The :file:`Battlefield 2 Server/python directory`
   - The Python directory of the current mod (e.g. :file:`Battlefield 2 Server/mods/bf2/python`)

      If the server switches mods, this will be changed, too. (The BF2 engine cannot automatically switch mods between rounds. Once a mod loads, it stays active until the server is manually stopped, reconfigured, and restarted.)

   - The ``Battlefield 2 Server/admin`` directory.

#. The BF2 engine imports the :py:mod:`bf2` package (the code for this package is located in the directory :file:`Battlefield 2 Server/python`).
#. When Python imports a package, it runs the :file:`_init_.py` module within it. For the :py:mod:`bf2` package, the ``_init_`` module imports and sets up the core code and objects for the game. This includes ``game.scoringCommon`` from the active mod's Python directory, which seems to be the only mod-specific Python code loaded here.
#. The BF2 engine calls :py:func:`bf2.init_module`

   - That method imports the stats modules
   - It's unclear why this is done separately instead of within the ``_init_`` module.

#. The BF2 engine processes the :file:`Battlefield 2 Server/mods/bf2/settings/ServerSettings.con` configuration file. By default, this file includes the directive ``sv.adminScript "default"``, which imports the ``default`` module from :file:`Battlefield 2 Server/admin`. This module mainly manages the ``RCon`` interface. It also has an ``init()`` function that, when called by the game engine, imports the ``admin.standard_admin`` package. This package currently handles team autobalancing and punishing team killing (TK).

   .. seealso::

      See the :doc:`Admin Module <../admin/module>` for more details.

#. During startup, as packages and modules load into the Python interpreter, they register to receive notifications (callbacks) when different :doc:`events <reference/events>` happen in the BF2 engine.
#. Some modules need to initialize before each round. They do this by registering for :py:func:`GameStatusChangedEvent`. When they receive this event and the game status is :py:attr:`~bf2.GameStatus.PreGame`, they run their initialization code.
#. Once setup is complete and the game is running, the Python code initialized during startup operates in an event-driven way. The game engine sends events to Python handlers that have registered for them. For instance, when a player is killed, a :py:func:`PlayerKilled` event triggers, and any modules registered for this event (like a scoring module) are called.
#. When a game round ends, the game engine and the embedded Python interpreter do **not** restart. This means :py:mod:`bf2` packages are **not** reimported or reinitialized. Instead, modules that need to clean up after a round register for :py:func:`GameStatusChangedEvent` during startup. When they detect the game status changes to :py:attr:`~bf2.GameStatus.EndGame`, they perform their cleanup.
#. The game engine then returns to an earlier stage where the game status changes to :py:attr:`~bf2.GameStatus.PreGame`. At this point, pre-game initialization handlers are called to restart the cycle.

.. note::

   The :file:`Battlefield 2 Server` directory also contains :file:`adminutils`, another Python code directory that the game engine does **not** use. This directory holds source code and executables for :file:`rotate_demo` and :file:`remoteconsole`, which are standalone applications. They serve as examples for creating software that interacts with BF2. Their Python origin is just a coincidence. (The BF2 engine manages ``RCon`` and demo recording internally, without the Python interpreter, though events related to these functions can be used to integrate your own Python code.)
