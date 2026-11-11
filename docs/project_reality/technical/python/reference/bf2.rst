BF2 Module
==========

.. py:module:: bf2

.. py:data:: g_debug

   A global flag (1 for active, 0 for inactive) that controls whether debugging information is printed across all BF2 Python modules.

.. py:function:: init_module()

   Initializes the BF2 Python environment. This function is called by the game engine during startup.

.. py:class:: GameStatus

   This class holds constant values that represent different game states. These values are returned by callbacks from the :py:func:`GameStatusChangedEvent` event.

   .. py:attribute:: Playing
   .. py:attribute:: EndGame
   .. py:attribute:: PreGame
   .. py:attribute:: Paused
   .. py:attribute:: RestartServer
   .. py:attribute:: NotConnected

   You must ``import`` :py:mod:`bf2` to access these class attributes.

.. py:class:: gameLogic

   This class provides a Python-friendly interface to many core BF2 engine functionalities, making them easier to access and use. The :py:mod:`bf2` module automatically creates a single instance of this class, named :py:class:`gameLogic`, when it starts.

   You must ``import`` :py:mod:`bf2` to access the methods and attributes of this object.

   .. py:method:: getModDir()

      :return: The directory of the current mod.
      :rtype: str

   .. py:method:: getMapName()

      :return: The name of the current map.
      :rtype: str

   .. py:method:: getWorldSize()

      :return: The north/south/east/west dimensions of the current map, in meters
      :rtype: tuple

   .. py:method:: getTeamName(team)

      :param team: The team number (0 or 1).
      :type team: int
      :return: The name of the specified team.
      :rtype: str

   .. py:method:: isAIGame()

      :return: True if the game is an AI-only game, False otherwise.
      :rtype: bool

   .. py:method:: sendServerMessage(playerId, message)

      Sends a message to a specific player on the server.

      :param playerId: The ID of the player.
      :type playerId: int
      :param message: The message to send.
      :type message: str

   .. py:method:: getTicketState(team)

      :param team: The team number (0 or 1).
      :type team: int
      :return: The current ticket state for the team.
      :rtype: int

   .. py:method:: setTicketState(team, value)

      Sets the ticket state for a team.

      :param team: The team number (0 or 1).
      :type team: int
      :param value: The new ticket state value.
      :type value: int

   .. py:method:: getTickets(team)

      :param team: The team number (0 or 1).
      :type team: int
      :return: The current number of tickets for the team.
      :rtype: int

   .. py:method:: setTickets(team, value)

      Sets the number of tickets for a team.

      :param team: The team number (0 or 1).
      :type team: int
      :param value: The new number of tickets.
      :type value: int

   .. py:method:: getDefaultTickets(team)

      :param team: The team number (0 or 1).
      :type team: int
      :return: The default number of tickets for the team.
      :rtype: int

   .. py:method:: getTicketChangePerSecond(team)

      :param team: The team number (0 or 1).
      :type team: int
      :return: The ticket change rate per second for the team.

   .. py:method:: setTicketChangePerSecond(team, value)

      Sets the ticket change rate per second for a team.

      :param team: The team number (0 or 1).
      :type team: int
      :param value: The new ticket change rate per second.

   .. py:method:: getTicketLimit(team, id)

      :param team: The team number (0 or 1).
      :type team: int
      :param id: The ticket limit ID.
      :type id: int
      :return: The ticket limit for the specified team and ID.
      :rtype: int

   .. py:method:: setTicketLimit(team, id, value)

      Sets a ticket limit for a team.

      :param team: The team number (0 or 1).
      :type team: int
      :param id: The ticket limit ID.
      :type id: int
      :param value: The new ticket limit value.
      :type value: int

   .. py:method:: getDefaultTicketLossPerMin(team)

      :param team: The team number (0 or 1).
      :type team: int
      :return: The default ticket loss per minute for the team.

   .. py:method:: getDefaultTicketLossAtEndPerMin()

      :return: The default ticket loss per minute at the end of the game.

   .. py:method:: getWinner()

      :return: The team that won the game.

   .. py:method:: getVictoryType()

      :return: The type of victory (e.g., ticket win, time limit win).

   .. py:method:: setTeamVehicleDamagePointLimit(value)

      Sets the percentage of team damage required to trigger a :py:func:`PlayerTeamDamagePoint` event.

      :param value: The percentage value (0-100).
      :type value: int

   .. py:method:: getObjectsOfType(objectType)

      :param objectType: The type of object to retrieve (e.g., 'C4Object', 'dice.bf.ControlPoint', etc.).
      :type objectType: str
      :return: A list of objects matching the specified type.
      :rtype: list

   .. py:method:: getObjectsOfTemplate(objectTemplate)

      :param objectTemplate: The template name of the object to retrieve (e.g., 'deployable_fob').
      :type objectTemplate: str
      :return: A list of objects matching the specified template.
      :rtype: list

.. py:class:: playerManager

   This class provides a Python-friendly interface to player management functions within the BF2 engine, including some additional calculations and logic. The :py:mod:`bf2` module automatically creates a single instance of this class, named :py:class:`playerManager`, when it starts.

   You must ``import`` :py:mod:`bf2` to access the methods and attributes of this object.

   .. py:method:: getNumberOfPlayers()

      :return: The total number of players currently connected to the server.
      :rtype: int

   .. py:method:: getNumberOfPlayersInTeam(team)

      :param team: The team number (0 or 1).
      :type team: int
      :return: The number of players in the specified team.
      :rtype: int

   .. py:method:: getNumberOfAlivePlayersInTeam(team)

      :param team: The team number (0 or 1).
      :type team: int
      :return: The number of alive players in the specified team.
      :rtype: int

   .. py:method:: getCommander(team)

      :param team: The team number (0 or 1).
      :type team: int
      :return: The player object representing the current commander.
      :rtype: bf2.PlayerManager.Player

   .. py:method:: getPlayers()

      :return: A list of current player objects.
      :rtype: list[bf2.PlayerManager.Player]

   .. py:method:: getPlayerByIndex(index)

      :param index: The 0-based index of the player.
      :type index: int
      :return: The player object at the specified index, or None if the index is invalid.
      :rtype: bf2.PlayerManager.Player or None

   .. py:method:: getNextPlayer(index)

      :param index: The 0-based index of the player.
      :type index: int
      :return: The player object at the next index (wrapping around if necessary), or None if the index is invalid.
      :rtype: bf2.PlayerManager.Player or None

   .. py:method:: enableScoreEvents()

      Enables PlayerScore events

   .. py:method:: disableScoreEvents()

      Disables PlayerScore events

.. py:class:: serverSettings

   This class provides a Python-friendly interface to various server settings within the BF2 engine. The :py:mod:`bf2` module automatically creates a single instance of this class, named :py:class:`serverSettings`, when it starts.

   You must ``import`` :py:mod:`bf2` to access the methods and attributes of this object.

   .. py:method:: getTicketRatio()

      :return: The current ticket ratio between teams.
      :rtype: float

   .. py:method:: getTeamRatioPercent()

      :return: The current team ratio percentage.
      :rtype: float

   .. py:method:: getMaxPlayers()

      :return: The maximum number of players allowed on the server.
      :rtype: int

   .. py:method:: getGameMode()

      :return: The current game mode name.
      :rtype: str

   .. py:method:: getMapName()

      :return: The name of the current map.
      :rtype: str

   .. py:method:: getTimeLimit()

      :return: The time limit for the current round in seconds.

   .. py:method:: getScoreLimit()

      :return: The score limit for the current round.

   .. py:method:: getAutoBalanceTeam()

      :return: Value indicating if auto team balancing is enabled.

   .. py:method:: getTKPunishEnabled()

      :return: Value indicating if teamkill punishment is enabled.

   .. py:method:: getTKNumPunishToKick()

      :return: The number of teamkills required to kick a player.

   .. py:method:: getTKPunishByDefault()

      :return: Value indicating if teamkill punishment is enabled by default.

   .. py:method:: getUseGlobalRank()

      :return: Value indicating if global ranks are used.

   .. py:method:: getUseGlobalUnlocks()

      :return: Value indicating if global unlocks are used.

   You cannot find out server name, port and other similar information this way. Instead, use f.e. :py:meth:`host.rcon_invoke` (``'sv.serverName'``) to get the server name.
