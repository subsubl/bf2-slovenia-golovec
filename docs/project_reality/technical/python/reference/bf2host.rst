
BF2 Host
========

.. py:module:: host

The :py:mod:`host` object serves as the interface between the main BF2 engine (written in C++) and Python modules. While most :py:mod:`host` methods are generally not used directly within Python modules (as standard BF2 Python modules like :py:class:`bf2.gameLogic` provide object-oriented wrappers), they are available for direct access.

You must ``import`` :py:mod:`host` to access the methods and attributes described here.

Event Handler Methods
---------------------

.. py:method:: registerHandler(event, handler, always_call=False)

   Registers a function to handle a specific event. If ``alwaysCall`` is not specified, the handler will only be invoked when the game is in the :py:attr:`bf2.GameStatus.Playing` state (not during :py:attr:`bf2.GameStatus.PreGame` or :py:attr:`bf2.GameStatus.EndGame`). To ensure it runs in :py:attr:`bf2.GameStatus.PreGame` and :py:attr:`bf2.GameStatus.EndGame` as well, ``alwaysCall`` must be specified and evaluate to true (e.g., "1").

   :param event: The name of the event to register a handler for.
   :type event: str
   :param handler: The callback function to execute when the event occurs.
   :type handler: Callable
   :param always_call: If true, the callback will run in all game states, not just in `playing`. Defaults to False.
   :type always_call: Union[bool, int]
   :return: None.
   :rtype: None

.. py:method:: registerGameStatusHandler(handler)

   Registers a function to handle game status events.

   :param handler: The callback function to execute on game status changes.
   :type handler: Callable[[GameStatus], None]
   :return: None.
   :rtype: None

.. py:method:: unregisterGameStatusHandler(handler)

   Unregisters a function that handles game status events.

   :param handler: The callback function to unregister.
   :type handler: Callable[[GameStatus], None]
   :return: None.
   :rtype: None

Trigger Methods
---------------

.. py:method:: trig_create(obj, callback, obj_name, radius, is_hemispherical, data)

   Creates a new trigger.

   :param obj: The object associated with the trigger.
   :type obj: int
   :param callback: The function to be called when the trigger is activated.
   :type callback: Callable
   :param obj_name: The name of the trigger object.
   :type obj_name: str
   :param radius: The radius of the trigger.
   :type radius: int
   :param is_hemispherical: An unknown boolean parameter.
   :type is_hemispherical: int
   :param data: Additional data to be passed to the callback.
   :type data: Any
   :return: The ID of the created trigger.
   :rtype: int

.. py:method:: trig_getObjects(trig_id)

   Retrieves all objects currently within the specified trigger's radius.

   :param trig_id: The ID of the trigger.
   :type trig_id: int
   :return: A list of objects within the trigger's radius.
   :rtype: list[int]

.. py:method:: trig_destroyAll()

   Destroys all currently active triggers.

   :return: None.
   :rtype: None

.. py:method:: trig_destroy(trig_id)

   Destroys a specific trigger by its ID.

   :param trig_id: The ID of the trigger to destroy.
   :type trig_id: int
   :return: None.
   :rtype: None

Global Stats Methods
--------------------

.. py:method:: pers_gamespyStatsNewGame()

   Initializes GameSpy statistics tracking for a new game.

   :return: None.
   :rtype: None

.. py:method:: pers_gamespyStatsEndGame()

   Finalizes and sends GameSpy statistics for the concluded game.

   :return: None.
   :rtype: None

.. py:method:: pers_gamespyStatsSendSnapshotFinal(snapShot)

   Sends the final snapshot of game statistics to GameSpy.

   :param snapShot: The final game snapshot data.
   :type snapShot: Any
   :return: None.
   :rtype: None

.. py:method:: pers_gamespyStatsSendSnapshotUpdate()

   Sends an update snapshot of game statistics to GameSpy.

   :return: None.
   :rtype: None

.. py:method:: pers_getStatsKeyVal(key)

   Retrieves a specific statistical value using its key.

   :param key: The key to retrieve the stat value for.
   :type key: str
   :return: The value associated with the given stat key.

.. py:method:: pers_plrRequestAwards(playerIndex, unknown1, unknown2)

   Requests awards for a specific player.

   :param playerIndex: The index of the player.
   :type playerIndex: int
   :param unknown1: An unknown parameter.
   :type unknown1: Any
   :param unknown2: An unknown parameter.
   :type unknown2: Any
   :return: None.
   :rtype: None

.. py:method:: pers_plrSetUnlocks(playerIndex, unknown1, unknown2)

   Sets the unlock status for a specific player.

   :param playerIndex: The index of the player.
   :type playerIndex: int
   :param unknown1: An unknown parameter.
   :type unknown1: Any
   :param unknown2: An unknown parameter.
   :type unknown2: Any
   :return: None.
   :rtype: None

.. py:method:: pers_plrAwardMedal()

   Awards a medal to a player (details of parameters and return value are unclear from context).

   :return: None.
   :rtype: None

.. py:method:: pers_plrRequestStats(playerIndex, unknown, urlToStatType)

   :return: Specified stat of the specified player
   :rtype: Any
   :param playerIndex: The index of the player.
   :type playerIndex: int
   :param unknown: An unknown parameter.
   :type unknown: Any
   :param urlToStatType: The type of stat to request.
   :type urlToStatType: str

.. py:method:: pers_plrRequestUnlocks(playerIndex, unknown)

   :return: Specified player's unlocks
   :rtype: Any
   :param playerIndex: The index of the player.
   :type playerIndex: int
   :param unknown: An unknown parameter.
   :type unknown: Any

``sh`` Methods (SwiffHost?)
---------------------------

.. py:method:: sh_setEnableCommander(bool_param)

   Enables or disables the commander position in the game.

   :param bool_param: Enable or disable the commander.
   :type bool_param: bool
   :return: None.
   :rtype: None

``gl`` Methods (GameLogic?)
---------------------------

.. py:method:: gl_sendEndOfRoundData(dataString)

   Presumably sends statistics-related information to clients when a round concludes.

   :param dataString: The data string containing end-of-round information.
   :type dataString: str
   :return: None.
   :rtype: None

``sgl`` Methods (ServerGameLogic?)
----------------------------------

.. py:method:: sgl_getSettingsBool()

   Retrieves the boolean value of a server setting. The specific setting is determined by context or implicit usage.

   :return: A boolean indicating the status of a specific setting.

.. py:method:: sgl_sendTextMessage(player_id, _p1, _p2, message, _p3=None)

   Sends a server message to a single player.

   .. important::

      The working status of this method is unknown.

   :param player_id: The ID of the player to send the message to.
   :type player_id: int
   :param _p1: An internal parameter.
   :type _p1: Any
   :param _p2: An internal parameter.
   :type _p2: Any
   :param message: The message content to send.
   :type message: str
   :param _p3: An optional parameter.
   :type _p3: Optional[Any]
   :return: Server message status or confirmation.
   :rtype: str

.. py:method:: sgl_sendRankEvent(player_idx, event, data)

   Sends a rank event to the game logic, presumably for logging or game state updates.

   :param player_idx: The index of the player.
   :type player_idx: int
   :param event: The player's rank.
   :type event: int
   :param data: The player's score.
   :type data: Any
   :return: None.
   :rtype: None

.. py:method:: sgl_sendMedalEvent(player_idx, event, value)

   Sends a medal event to the game logic.

   :param player_idx: The index of the player.
   :type player_idx: int
   :param event: The type of medal event.
   :type event: int
   :param value: The value associated with the medal event.
   :type value: int
   :return: None.
   :rtype: None

.. py:method:: sgl_sendPythonEvent(player_idx, command, args)

   Sends a custom event from Python to the server game logic. The exact parameters and data format are not specified.

   :param player_idx: The index of the player associated with the event.
   :type player_idx: int
   :param command: The command or type of event.
   :type command: int
   :param args: Additional data payload for the event.
   :type args: Tuple[Any]
   :return: None.
   :rtype: None

.. py:method:: sgl_sendGameLogicEvent(player_idx, event, data)

   Sends a general game logic event.

   :param player_idx: The ID of the player associated with the event.
   :type player_idx: int
   :param event: The name or type of the game logic event.
   :type event: int
   :param data: Additional data payload for the event.
   :type data: Any
   :return: None.
   :rtype: None

.. py:method:: sgl_sendHudEvent(player_idx, event, data)

   Sends an event to update or trigger an action on a player's Heads-Up Display (HUD).

   :param player_idx: The ID of the player to which the HUD event is directed.
   :type player_idx: int
   :param event: The type of HUD event.
   :type event: int
   :param data: Data associated with the HUD event.
   :type data: Any
   :return: None.
   :rtype: None

.. py:method:: sgl_getIsAIGame()

   :return: Indicates whether the current game includes AI players.
   :rtype: bool

.. py:method:: sgl_getControlPointsInGroup()

   Retrieves control points that belong to a specific group (group identifier is not specified).

   :return: None.
   :rtype: None

.. py:method:: sgl_getParam(name, unknown1, unknown2)

   Retrieves a server setting parameter by name.

   :param name: The name of the parameter to retrieve.
   :type name: str
   :param unknown1: An unknown parameter.
   :type unknown1: Any
   :param unknown2: An unknown parameter.
   :type unknown2: Any
   :return: The value of the specified parameter.
   :rtype: Any

.. py:method:: sgl_setParam(name, unknown1, unknown2, unknown3)

   Sets a server setting parameter by name.

   :param name: The name of the parameter to set.
   :type name: str
   :param unknown1: An unknown parameter.
   :type unknown1: Any
   :param unknown2: An unknown parameter.
   :type unknown2: Any
   :param unknown3: The new value for the parameter.
   :type unknown3: Any
   :return: None.
   :rtype: None

.. py:method:: sgl_endGame(winner, victoryType)

   Presumably ends the current game, declaring ``winner`` and ``victoryType``.

   :param winner: The winner of the game.
   :type winner: int
   :param victoryType: The type of victory.
   :type victoryType: int
   :return: None.
   :rtype: None

.. py:method:: sgl_getWorldSize()

   :return: The approximate north/south/east/west dimensions of the current map in meters.
   :rtype: tuple

.. py:method:: sgl_getMapName()

   :return: Current map name
   :rtype: str

.. py:method:: sgl_getModDirectory()

   :return: Directory containing the currently active mod
   :rtype: str

``ss`` Methods (Server Settings?)
---------------------------------

.. py:method:: ss_getParam(parameter)

   Note that server name, port, and similar information cannot be retrieved this way. Instead, use methods like :py:meth:`host.rcon_invoke` to get the server name.

   :param parameter: The name of the setting to retrieve.
   :type parameter: str
   :return: The value of the specified setting.

   Settings include:

   - ``ticketRatio``
   - ``teamRatioPct``
   - ``maxPlayers``
   - ``gameMode``
   - ``mapName``
   - ``timeLimit``
   - ``scoreLimit``
   - ``autoBalance``
   - ``tkpEnabled``
   - ``tkpNeeded``
   - ``tkpDefault``
   - ``globRank``
   - ``globUnlocks``

Object Manager Methods
----------------------

.. py:method:: omgr_getObjectsOfTemplate(template)

   Retrieves all objects in the game that are instances of a given template.

   :param template: The template name to filter objects by.
   :type template: Any
   :return: A list of objects matching the specified template.
   :rtype: list[Any]

.. py:method:: omgr_getObjectsOfType(type)

   Retrieves all objects in the game of a specific type.

   :param type: The type of object to filter by.
   :type type: Any
   :return: A list of objects matching the specified type.
   :rtype: list[Any]

Timer Methods
-------------

.. py:method:: timer_created(timer)

   Acknowledges the creation of a timer.

   :param timer: The timer object that has been created.
   :type timer: Any

.. py:method:: timer_getTimers()

   .. warning::

      **Do not use; this is unfinished DICE code.**
      Attempting to access other slots will crash the server.

   :return: A tuple that only populates one slot.
   :rtype: tuple

.. py:method:: timer_destroy(timer)

   Destroys a specific timer.

   :param timer: The timer object to destroy.
   :type timer: Any
   :rtype: None

.. py:method:: timer_getWallTime()

   See :doc:`BF2 Time <../../engine/time>`.

   :return: The number of seconds that have passed since the server started.
   :rtype: int

Player Manager Methods
----------------------

.. py:method:: pmgr_enableScoreEvents(value)

   Enables score event tracking for players.

   :param value: The value to set for enabling score events.
   :type value: int
   :return: None.
   :rtype: None

.. py:method:: pmgr_getScore(playerIndex, name)

   :return: The score value for the specified player and score name.
   :rtype: int
   :param playerIndex: The index of the player.
   :type playerIndex: int
   :param name: The name of the score to retrieve.
   :type name: str

.. py:method:: pmgr_setScore(playerIndex, name, value)

   :return: The score name of the specified player.
   :rtype: None
   :param playerIndex: The index of the player.
   :type playerIndex: int
   :param name: The name of the score to set.
   :type name: str
   :param value: The new score value.
   :type value: int

.. py:method:: pmgr_p_get(name, playerIndex, default=None)

   Retrieves a specific property of a player.

   :param name: The name of the player property to retrieve.
   :type name: str
   :param playerIndex: The index of the player.
   :type playerIndex: int
   :param default: The default value to return if the property is not found.
   :type default: Optional[Any]
   :return: The value of the specified player property.
   :rtype: Any

.. py:method:: pmgr_p_set(name, playerIndex, value)

   Sets a specific property of a player.

   :param name: The name of the player property to set.
   :type name: str
   :param playerIndex: The index of the player.
   :type playerIndex: int
   :param value: The new value for the player property.
   :type value: Any
   :return: None.
   :rtype: None

.. py:method:: pmgr_isIndexValid(index)

   :return: Whether the specified player index is valid.
   :rtype: bool
   :param index: The player index to check.
   :type index: int

.. py:method:: pmgr_getCommander(team_idx)

   :return: The player object representing the current commander.
   :rtype: int
   :param team_idx: The index of the team for which to get the commander.
   :type team_idx: int

.. py:method:: pmgr_getPlayers()

   :return: A list of current player objects.
   :rtype: list[int]

.. py:method:: pmgr_getNumberOfPlayers()

   :return: The total number of players currently in the game.
   :rtype: int

``RCon`` Methods
----------------

.. py:method:: rcon_invoke(command)

   Executes a server console command.

   :param command: The server console command to execute.
   :type command: str
   :rtype: str

.. py:method:: rcon_feedback(playerid, message)

   Sends a message to an in-game player's RCon client.

   :param playerid: The ID of the player to send the message to.
   :type playerid: int
   :param message: The message content.
   :type message: str
   :return: None.
   :rtype: None

Logging Methods
---------------

.. py:method:: log(message)

   Sends a message to the game log.

   :param message: The message to send to the log.
   :type message: str
   :return: None.
   :rtype: None
