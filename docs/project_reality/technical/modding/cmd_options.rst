
Command Line Options
====================

Battlefield 2 offers many command line options. You might already know some, like ``+fullscreen 1``. To use these options, open a shortcut's properties, go to the 'Shortcut' tab, and add the option to the end of the 'Target' field. Since options are set on shortcuts, you can create multiple shortcuts, each with different settings. The following is a list of known command line options.

.. note::

   These options were found using a special debug version of BF2.exe. Some might not work with the regular BF2.exe. You can get the debug version by installing the Battlefield 2 Editor; it's called BF2_r.exe in your main Battlefield 2 directory. You can download the editor at `Battlefield 2 Editor <http://www.fileplanet.com/155852/download/Battlefield-2-Editor>`_. Also, remember that these options are case-sensitive.

Basic Options
-------------

.. list-table::
   :header-rows: 1

   * - Command
     - Description
     - Usage
   * - ``+multi``
     - Lets you run multiple Battlefield 2 games at the same time.
     - ``+multi``
   * - ``+joinServer``
     - Connects to a specific server. You can use either the server's IP address or its hostname.
     - ``+joinServer`` ``OR``
   * - ``+playerName``
     - Sets your player name.
     - ``+playerName``
   * - ``+password``
     - Use this with ``+joinServer`` if the server needs a password. It might also set the password for a dedicated server.
     - ``+password``
   * - ``+lowPriority``
     - Makes Battlefield 2 run with lower CPU priority, which means less CPU usage but also lower performance.
     - ``+lowPriority``
   * - ``+loadLevel``
     - Loads a specific level.
     - ``+loadLevel``
   * - ``+wx``
     - When Battlefield 2 is in windowed mode, this sets the window's horizontal position. 0 is the far left of the screen, and the window is positioned from its left edge.
     - ``+wx``
   * - ``+wy``
     - When Battlefield 2 is in windowed mode, this sets the window's vertical position. 0 is the very top of the screen, and the window is positioned from its top edge.
     - ``+wy``
   * - ``+szx``
     - When Battlefield 2 is in windowed mode, this sets the window's width.
     - ``+szx``
   * - ``+szy``
     - When Battlefield 2 is in windowed mode, this sets the window's height.
     - ``+szy``
   * - ``+loadObfuscated``
     - Loads scrambled shaders. The exact purpose is unclear.
     - ``+loadObfuscated``
   * - ``+fullscreen``
     - Switches Battlefield 2 between windowed and full-screen modes.
     - ``+fullscreen``
   * - ``+noSound``
     - Starts Battlefield 2 without any sound.
     - ``+noSound``
   * - ``+lateLoading``
     - If set to 1, game resources (currently only sound) will load only when they are first used.
     - ``+lateLoading``
   * - ``+skipMips``
     - Determines how many mip-levels to skip in textures.
     - ``+skipMips``
   * - ``+mergeMaterials``
     - Combines materials when the game loads.
     - ``+mergeMaterials``
   * - ``+managedTextures``
     - Controls whether system memory is used for textures.
     - ``+managedTextures``
   * - ``+debugOutput``
     - Turns debug messages on or off.
     - ``+debugOutput``
   * - ``+demo``
     - Sets the configuration file for demo options. Its exact function is unclear.
     - ``+demo <??>``
   * - ``+pyVerbose``
     - Shows detailed output from Python scripts. Not very interesting.
     - ``+pyVerbose``
   * - ``+modPath``
     - Sets the path where Battlefield 2 looks for mods. Usually, this is :file:`mods/bf2`.
     - ``+modPath``
   * - ``+ignoreAsserts``
     - Ignores debug assertion errors. Only works if ``+developer 1`` or ``+dedicated 1`` is also used.
     - ``+ignoreAsserts``
   * - ``+disableShaderCache``
     - Turns off the shader cache. This should only be used with ``+developer 1``.
     - ``+disableShaderCache``
   * - ``+dumpAllConFiles``
     - Writes the names of all :file:`.con` files to :file:`mods/$MOD$/allConFiles.con`.
     - ``+dumpAllConFiles``
   * - ``+customConFile``
     - Uses a specific :file:`.con` file instead of loading all of them. This file should use the ``run`` command to specify which other :file:`.con` files to execute.
     - ``+customConFile``
   * - ``+help``
     - Shows help information for command line options, including descriptions.
     - ``+help``
   * - ``+?``
     - Does the same thing as ``+help``.
     - ``+?``
   * - ``+fileMonitor``
     - Automatically updates files (like shaders) when they change. This could be very useful if it also applies to :file:`.con` files.
     - ``+fileMonitor``
   * - ``+playerPassword``
     - Sets the player's password.
     - ``+playerPassword``
   * - ``+developer``
     - Prevents automatic login and allows other command line options to be used with it.
     - ``+developer``
   * - ``+disableSwiff``
     - Turns off the Swiff player, which disables the Flash animations used in the main menu. Swiff refers to the :file:`.swf` Flash file format.
     - ``+disableSwiff``
   * - ``+debugSwiff``
     - Turns on debug output for Swiff. Swiff refers to the :file:`.swf` Flash file format.
     - ``+debugSwiff``
   * - ``+playNow``
     - Starts the game and automatically uses the 'Play Now' feature.
     - ``+playNow``
   * - ``+pbPath``
     - Sets the path to Punkbuster for setups with multiple game instances. This is usually :file:`{install_dir}/pb`.
     - ``+pbPath``
   * - ``+keepCollisionForNavMeshes``
     - Keeps collision mesh Level of Details (LODs) needed to create AI navigation meshes. The exact function is unclear.
     - ``+keepCollisionForNavMeshes``
   * - ``+restart``
     - Used by BF2 to restart the game without showing videos, for example, when switching mods. Can also be used to start BF2 without videos using your own shortcuts.
     - ``+restart``
   * - ``+port``
     - Used with ``+joinServer`` to specify the port number for connecting to a server.
     - ``+port``

Dedicated Server Options
------------------------

.. list-table::
   :header-rows: 1

   * - Command
     - Description
     - Usage
   * - ``+dedicated``
     - Starts Battlefield 2 as a dedicated server. This is not needed on Linux.
     - ``+dedicated``
   * - ``+port``
     - Sets the port number the server should use.
     - ``+port``
   * - ``+maxPlayers``
     - Sets the maximum number of players allowed on the server.
     - ``+maxPlayers``
   * - ``+gameMode``
     - Sets the game mode for the server.
     - ``+gameMode``
   * - ``+config``
     - Sets the path to the :file:`ServerSettings.con` file to use.
     - ``+config``
   * - ``+mapList``
     - Sets the path to the :file:`mapList.con` file to use.
     - ``+mapList``
   * - ``+noStatusMonitor``
     - Use this if you don't want to run BF2 inside a screen session.
     - ``+noStatusMonitor`` with values 1 (or 0 the default if you don't specify this option at all)
   * - ``+ranked``
     - Allows sending game data to Gamespy. This setting only works if EA has the server's IP address in their database.
     - ``+ranked``

Advanced Options
----------------

.. list-table::
   :header-rows: 1

   * - Command
     - Description
     - Usage
   * - ``+hostServer``
     - Currently unknown. Likely starts a local server.
     - ``+hostServer <??>``
   * - ``+checkForAvailablePatch``
     - Currently unknown. Likely checks for available patches. When used with the debug version, it causes an error on startup and appears to be broken.
     - ``+checkForAvailablePatch <??>``
   * - ``+checkForPatch``
     - Currently unknown. How this differs from ``+checkForAvailablePatch`` is unclear. When used with the debug version, it causes an error on startup and appears to be broken.
     - ``+checkForPatch <??>``
   * - ``+aidll``
     - Currently unknown. Perhaps it enables or disables the Battlefield 2 :file:`aidll.dll` file.
     - ``+aidll <??>``
   * - ``+ai``
     - Forces Battlefield 2 to load AI bots, regardless of the map, requirements, or settings. --MasterX
     - ``+ai <0/1>``
   * - ``+refresh``
     - Currently unknown.
     - ``+refresh <??>``
   * - ``+renderMode``
     - Sets the current rendering mode. Possible values are 0-5, but their specific functions are not yet known.
     - ``+renderMode``
   * - ``+rp``
     - Currently unknown.
     - ``+rp <??>``
   * - ``+deviceType``
     - Currently unknown.
     - ``+deviceType <??>``
   * - ``+deviceBehavior``
     - Currently unknown.
     - ``+deviceBehavior <??>``
   * - ``+skipMeshLods``
     - Currently unknown. `LOD <http://en.wikipedia.org/wiki/Level_of_Detail>`_
     - ``+skipMeshLods <??>``
   * - ``+keepTemplates``
     - Currently unknown.
     - ``+keepTemplates <??>``
   * - ``+profileTextureUsage``
     - Currently unknown.
     - ``+profileTextureUsage <??>``
   * - ``+convertCollisionMeshes``
     - Currently unknown.
     - ``+convertCollisionMeshes <??>``
   * - ``+generateLightMaps``
     - Currently unknown.
     - ``+generateLightMaps <??>``
   * - ``+debugNetwork``
     - Currently unknown.
     - ``+debugNetwork <??>``
   * - ``+debugGhostManager``
     - Currently unknown.
     - ``+debugGhostManager <??>``
   * - ``+compile``
     - Currently unknown.
     - ``+compile <??>``
   * - ``+useCompiled``
     - Currently unknown.
     - ``+useCompiled <??>``
   * - ``+NoEffectTextureAtlas``
     - Currently unknown.
     - ``+NoEffectTextureAtlas <??>``
   * - ``+menu``
     - Currently unknown. This is used by Battlefield 2's default shortcut as ``+menu 1``.
     - ``+menu``
