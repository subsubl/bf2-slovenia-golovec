
Events
======

The interaction between the BF2 engine and Python programs is primarily `event-driven <https://en.wikipedia.org/wiki/Event-driven_programming>`_. This means that when a specific "event" occurs in the game, BF2 checks if any Python programs have registered to be notified of that event. If so, the registered Python functions (callbacks) are executed. You can think of these events as "hooks" into the game engine where you can attach your own Python code.

Multiple callbacks can be registered for a single event. When that event occurs, all registered callbacks will be executed. For instance, if three different programs are registered for the "PlayerConnect" event, all three will run when a new player connects.

Types of Events
---------------

The BF2 engine supports five types of events

These are events that occur during the normal course of gameplay. You register to receive callbacks for these events using the following syntax:

.. code-block:: python
   :caption: Registering a standard event handler

   host.registerHandler('EventName', pythonEventHandler[, parameter])

This registration is typically done within an object's ``init()`` method, but it can be placed anywhere in your code.

Game Status Events
~~~~~~~~~~~~~~~~~~

The BF2 engine generates these events when the game's status changes. You register to receive callbacks for these events as follows:

.. code-block:: python
   :caption: Registering a game status event handler

   host.registerGameStatusHandler(pythonEventHandler)

The possible game states (as defined in :py:class:`bf2.GameStatus`) are:

- NotConnected
- PreGame
- Playing
- Paused
- EndGame
- RestartServer

Game status events are typically used to initiate processes like pre-game setup or post-game cleanup.

Trigger Events
~~~~~~~~~~~~~~

"Trigger" events are activated when a vehicle enters a specified distance from an object. Triggers are created and registered using ``bf2.triggerManager``:

.. code-block:: python
   :caption: Creating trigger events

   createHemiSphericalTrigger(object, triggerEventHandler, objectName, radius[, data])

   bf2.triggerManager.createRadiusTrigger(object, triggerEventHandler, objectName, radius[, data])

In standard Battlefield 2, trigger events are used for tracking flag capture scoring (triggers activate when a player enters or leaves a fixed radius around each control point) and for environmental effects, such as birds taking flight when a player enters their trigger radius.

.. _timer-events:

Timer Events
~~~~~~~~~~~~

.. py:currentmodule:: host

.. py:method:: bf2.Timer(timerEventHandler, delta, alwaysTrigger[, data])

   Timer events are activated when a specific amount of time has passed.

   In standard Battlefield 2, timer events are used for periodic status checks related to scoring, ranking, punishing team kills, and other game mechanics.

   Refer to the :py:class:`bf2.Timer` class description for more details.

Descriptions of Events
----------------------

EA/DICE have not published a list of events, but here is a list of events that have been discovered so far.

.. py:function:: EventName(handlerParameter1, handlerParameter2, ...)

   ``EventName`` refers to the name of the event you register with ``host.registerHandler``. The parameters listed are those your event handler function should expect to receive when the event is triggered.

   :param playerObject: An instance of :py:class:`bf2.PlayerManager.Player`.
   :param playerID: Players are assigned unique ``playerID`` numbers, starting from "1", as they connect to the server.
   :param int squadID: Squads for each team are independently numbered, starting from "1". Players not in a squad, including team commanders, are assigned to squad "0".
   :param int teamID: ``0`` for US, ``1`` for China or MEC.

Server Events
~~~~~~~~~~~~~

.. py:function:: ServerReady()

   TBD

.. py:function:: BeginRound()

   TBD

.. py:function:: EndRound()

   TBD

Player Events
~~~~~~~~~~~~~

.. py:function:: PlayerConnect(playerObject)

   Fires when a player connects to the game.

.. py:function:: PlayerSpawn(playerObject, soldierObject)

   Occurs when a player spawns, linking a :py:class:`player` (the player's "spirit") with a :py:class:`soldierObject` (the player's "body").

.. py:function:: PlayerChangeTeams(playerObject, humanHasSpawned)

   :param humanHasSpawned: Is ``1`` if the player triggering the event is human (not AI). This event does not fire when a team change occurs due to ``setTeam``.

.. py:function:: PlayerChangeWeapon(playerObject, oldWeaponObject, newWeaponObject)

   Player has changed which weapon they are holding.

.. py:function:: PlayerChangedSquad(playerObject, oldSquadID, newSquadID)

   ``SquadID`` is ``0`` for players who are not part of any squad, including the team commander.

.. py:function:: PlayerScore(playerObject, difference)

   ``difference`` represents the change in the player's score (can be positive or negative).

.. py:function:: PlayerHealPoint(givingPlayerObject, receivingSoldierObject)

   Occurs when one player heals another. There is no indication of the amount of health restored.

.. py:function:: PlayerRepairPoint(givingPlayerObject, receivingVehicleObject)

   Occurs when a player repairs a vehicle. There is no indication of the amount of damage repaired.

.. py:function:: PlayerGiveAmmoPoint(givingPlayerObject, receivingPhysicalObject)

   Occurs when a player replenishes the ammunition of another player or vehicle. There is no indication of the amount of ammo replenished.

.. py:function:: PlayerTeamDamagePoint(playerObject, victimSoldierObject)

   Occurs when a player damages another player on their own team. There is no indication of the amount of damage inflicted.

.. py:function:: PlayerKilled(victimPlayerObject, attackerPlayerObject, weaponObject, assists, victimSoldierObject)

   This event occurs when a player is critically injured but can still be revived. If other players assisted in the kill, ``assists`` will be a tuple of tuples. The top-level tuple contains one lower-level tuple for each assisting player. Each lower-level tuple has two elements: a :py:class:`playerObject` for the assisting player and a number indicating the type of assist (1=targeting assist, 2=kill damage assist, 3=driver assist).

.. py:function:: PlayerRevived(revivedPlayerObject, medicPlayerObject)

   Occurs when a player, critically injured, is restored to full health by a medic using "shock paddles." Players can only be revived between a :py:func:`PlayerKilled` event and a subsequent :py:func:`PlayerDeath` event.

.. py:function:: PlayerDeath(playerObject, soldierObject)

   This event occurs when a player is definitively dead and cannot be revived; they will only return to the game by respawning. The :py:class:`soldierObject` represents the discarded soldier "body," while the :py:class:`playerObject` represents the player's "spirit," which persists through the next spawn.

.. py:function:: PlayerBanned(playerObject, time, type)

   TBD

.. py:function:: PlayerKicked(playerObject)

   Occurs when a player is removed from the server.

.. py:function:: PlayerDisconnect(playerObject)

   Occurs when a player disconnects from the server.

Vehicle and Kit Events
~~~~~~~~~~~~~~~~~~~~~~

.. py:function:: EnterVehicle(playerObject, vehicleObject[, freeSoldier])

   The player (represented by :py:class:`playerObject`) has entered the vehicle (represented by :py:class:`vehicleObject`). ``freeSoldier`` is ``1`` if the player is a passenger and can use their kit's weapons/objects (e.g., in seat 4+ of a Black Hawk).

.. py:function:: ExitVehicle(playerObject, vehicleObject)

   Occurs when a player exits a vehicle.

.. py:function:: VehicleDestroyed(vehicleObject, attackerObject)

   The :py:class:`vehicleObject` has been destroyed by the ``attackerObject``.

.. py:function:: PickupKit(playerObject, kitObject)

   Occurs when a player picks up a kit, either physically or when they spawn.

.. py:function:: DropKit(playerObject, kitObject)

   Occurs when a player drops a kit, either due to death or by picking up a different kit.

Team Events
~~~~~~~~~~~

.. py:function:: Reset(data)

   TBD

.. py:function:: ChangedCommander(teamID, oldCommanderPlayerObject, newCommanderPlayerObject)

   Occurs when a team's commander changes. The ``oldCommanderPlayerObject`` or ``newCommanderPlayerObject`` may be ``None``.

.. py:function:: ChangedSquadLeader(squadID, oldLeaderPlayerObject, newLeaderPlayerObject)

   Occurs when a squad's leader changes. The ``oldLeaderPlayerObject`` or ``newLeaderPlayerObject`` may be ``None``.

.. _game-events:

Game Events
~~~~~~~~~~~

.. py:function:: ControlPointChangedOwner(controlPointObject, attackingTeamID)

   TBD

.. py:function:: TimeLimitReached(value)

   This event fires when the round's fixed time limit expires (the meaning of "value" is unclear).

.. py:function:: TicketLimitReached(team, limitID)

   TBD

Command Events
~~~~~~~~~~~~~~

.. py:function:: ConsoleSendCommand(command, args)

   This event is triggered when someone uses the ``pythonHost.sendCommand`` console command. Unfortunately, this command/event mechanism appears to be disabled on non-ranked servers. As a workaround, you can achieve a similar effect by :doc:`creating and registering your own custom RCon commands <../../cookbook/new_rcon>`.
.. py:function:: RemoteCommand(playerId, cmd)

   This event fires when a game client issues an ``RCon`` (remote console) command. ``cmd`` is the command given by the player. This event is used by the admin module to receive and process ``RCon`` commands from players; however, ``RCon`` commands received directly from TCP connections by the admin module do not trigger this event.

.. py:function:: ClientCommand(command, issuerPlayerObject, args)

   This event occurs when a game client issues certain in-game commands. So far, the identified commands are: ``command=100`` (player wants to punish a teammate for teamkill) and ``command=101`` (player wants to forgive). In both cases, ``args=1``. This response is generated when the player responds to an on-screen prompt initiated by a call to the :py:meth:`bf2.gameLogic.sendClientCommand <bf2.GameLogic.GameLogic.sendClientCommand>` method.

Miscellaneous Events
~~~~~~~~~~~~~~~~~~~~

.. py:function:: PlayerUnlocksResponse(succeeded, player, unlocks)

   Unlocks are requested and received asynchronously. This event triggers when the response for a player (an object of type Player) is received. If the ranking server fails to find the player, ``succeeded`` is set to ``false``; otherwise, it's ``true``. ``unlocks`` is a list of kit IDs (e.g., 11, 22, 33...77).

.. py:function:: PlayerAwardsResponse()

   TBD

.. py:function:: ChatMessage(playerId, text, channel, flags)

   ``channel`` can be ``Squad``, ``Team``, ``Global``, ``ServerTeamMessage``, or ``ServerMessage``. ``text`` is the message content, prefixed by ``HUD_TEXT_CHAT_TEAM`` or ``HUD_TEXT_CHAT_SQUAD`` if sent to the Team or Squad channel, respectively; there is no prefix for Global messages. ``playerId`` is ``-1`` for all server messages. If the sender is dead, their message is also prefixed by ``HUD_CHAT_DEADPREFIX``. (Strings like ``HUD_TEXT_CHAT_TEAM``, ``HUD_CHAT_DEADPREFIX``, etc., are keys used by the game engine for localization.)

.. py:function:: PlayerStatsResponse(succeeded, player, response)

   TBD

.. py:function:: Update(data)

   TBD

Non-Standard Events
~~~~~~~~~~~~~~~~~~~

.. py:function:: GameStatusChangedEvent(status)

   This event type is registered using :py:meth:`host.registerGameStatusHandler`. ``status`` is an integer status code defined by :py:class:`bf2.GameStatus`.

.. py:function:: TriggerEvent(triggerID, object, vehicle, enter, userData)

   This event type is registered using :py:meth:`bf2.triggerManager.createHemiSphericalTrigger <bf2.TriggerManager.TriggerManager.createHemiSphericalTrigger>` or :py:meth:`bf2.triggerManager.createRadiusTrigger <bf2.TriggerManager.TriggerManager.createHemiSphericalTrigger>`. The trigger (``triggerID``) activates when a ``vehicle`` enters the preset radius of an ``object``.

.. py:function:: TimerEvent(data)

   This event fires when a timer, established with :py:class:`bf2.Timer`, expires. ``data`` is an optional piece of information (of any type) that can be set when the timer is created.

Mysterious Events
-----------------

These strings were found in the server executable and appear to be internal game engine events. They generally aren't accessible from Python, except in a few cases where there's a direct correspondence between these "events" and Python events (e.g., "BeginRoundEvent" might be the same as "BeginRound"). For more information, refer to :doc:`BF2 Internals <../../engine/internals>`.

.. py:function:: RemoveSpawnGroupEvent
.. py:function:: CreateSpawnGroupEvent
.. py:function:: ContentCheckEvent
.. py:function:: UAVEvent
.. py:function:: MissileInitEvent
.. py:function:: UnlockEvent
.. py:function:: MedalEvent
.. py:function:: ToggleFreeCameraEvent
.. py:function:: VoipSessionEvent
.. py:function:: RequestEvent
.. py:function:: PythonCommandEvent
.. py:function:: EndOfRoundEvent

   → EndRound

.. py:function:: BeginRoundEvent

   → BeginRound

.. py:function:: TargetDirectionEvent
.. py:function:: VoteEvent
.. py:function:: VoipPlayerMuteEvent
.. py:function:: SupplyDropEvent
.. py:function:: CommanderCamEvent
.. py:function:: VoipOnOffEvent
.. py:function:: AmbientEffectAreaEvent
.. py:function:: StickyProjectileEvent
.. py:function:: ArtilleryEvent
.. py:function:: SpottedEvent
.. py:function:: SetSquadLeaderEvent
.. py:function:: SetAcceptOrderEvent
.. py:function:: KickBanEvent
.. py:function:: RankEvent
.. py:function:: InviteEvent
.. py:function:: IssueSquadOrderEvent
.. py:function:: SetPrivateSquadEvent
.. py:function:: ChangeSquadNameEvent
.. py:function:: KilledByEvent
.. py:function:: RadioMessageEvent
.. py:function:: CommanderEvent
.. py:function:: LeaveSquadEvent
.. py:function:: JoinSquadEvent
.. py:function:: StringBlockEvent
.. py:function:: HandleDropEvent
.. py:function:: HandlePickupEvent
.. py:function:: ChangePlayerNameEvent
.. py:function:: PostRemoteEvent
.. py:function:: ExitVehicleEvent

   → ExitVehicle

.. py:function:: EnterVehicleEvent

   → EnterVehicle

.. py:function:: DestroyPlayerEvent
.. py:function:: DestroyObjectEvent
.. py:function:: CreateKitEvent
.. py:function:: CreateObjectEvent
.. py:function:: CreatePlayerEvent
.. py:function:: DataBlockEvent
.. py:function:: ConnectionTypeEvent
.. py:function:: ChallengeResponseEvent
.. py:function:: ChallengeEvent

Event Patterns
--------------

While each event documented here represents a distinct change in game state, certain in-game actions consistently trigger a fixed sequence of events. For example, a :py:func:`PlayerSpawn` event is always followed by a :py:func:`PlayerChangeWeapon` event and a :py:func:`PickupKit` event. This section outlines some of these recurring event patterns.

Player Spawn
~~~~~~~~~~~~

#. :py:func:`PlayerConnect`
#. :py:func:`PlayerSpawn`

   The player becomes associated with a :py:class:`soldierObject`.

#. :py:func:`PlayerChangeWeapon`

   Changes from ``None`` to a :py:class:`weaponObject`.

#. :py:func:`PickupKit`

Player Killed
~~~~~~~~~~~~~

#. :py:func:`PlayerKilled`
#. :py:func:`PlayerScore`
#. :py:func:`DropKit`

   The victim drops their kit.

#. :py:func:`ExitVehicle`

   If the player was inside a vehicle.

#. :py:func:`PlayerDeath`

Player Revived
~~~~~~~~~~~~~~

#. :py:func:`PlayerKilled`
#. :py:func:`PlayerScore`

   For the attacker.

#. :py:func:`DropKit`

   The victim drops their kit.

#. :py:func:`PlayerRevived`
#. :py:func:`PickupKit`

   The revived player picks up the nearest kit (ideally their old one, but not necessarily); if no kit is nearby, they default to an "assault" kit.

#. :py:func:`PlayerScore`

   For the medic who performed the revive.

Flag Change
~~~~~~~~~~~

#. :py:func:`ControlPointChangedOwner`

   When the flag is neutralized.

#. :py:func:`PlayerScoreEvent`

   Score awarded for neutralizing the flag, repeated for each attacker within the Control Point (CP) radius.

#. :py:func:`ControlPointChangedOwner`

   When the capture is complete.

#. :py:func:`PlayerScoreEvent`

   Score awarded for completing the capture, repeated for each attacker within the CP radius.

Player Kicked
~~~~~~~~~~~~~

#. :py:func:`PlayerKicked`
#. :py:func:`DropKit`
#. :py:func:`PlayerDeath`
#. :py:func:`PlayerDisconnect`

Player Banned
~~~~~~~~~~~~~

#. :py:func:`PlayerBanned`
#. :py:func:`PlayerKicked`
#. :py:func:`DropKit`
#. :py:func:`PlayerDeath`
#. :py:func:`PlayerDisconnect`

Overall Game State Change
~~~~~~~~~~~~~~~~~~~~~~~~~

#. :py:func:`StatusChange`

   Changes to ``PreGame``.

#. :py:func:`Reset`

   This event does not occur in the first round after a server starts.

#. :py:func:`StatusChange`

   Changes to ``Playing``; remains in this state until enough players connect.

#. :py:func:`StatusChange`

   Changes to ``PreGame`` once enough players have connected.

#. :py:func:`Reset`
#. :py:func:`StatusChange`

   Changes to ``Playing`` – the actual game round now begins.

#. Gameplay proceeds, starting with players spawning in.

#. :py:func:`StatusChange`

   Changes to ``EndGame``.

#. :py:func:`DropKit`

   For every player still in the game at the end.
