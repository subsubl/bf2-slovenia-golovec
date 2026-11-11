BF2 Objects
===========

.. py:class:: player

   An object of this class is created for each player in the game. Upon initialization, each :py:class:`player` object automatically creates a :py:class:`score` object and assigns it to its ``score`` attribute.

   While you can create :py:class:`player` objects by importing :py:class:`playerManager` (e.g., ``x = PlayerManager.Player(index)``), you'll typically access methods and attributes of existing :py:class:`player` objects returned by other calls, which doesn't require a special import statement.

   .. code-block:: python
      :caption: Instance creation

      x = PlayerManager.Player(index)

   .. py:attribute:: index

      The unique numerical index of this player on the server.

   .. py:method:: isValid()

      :return: ``True`` if the player object is currently valid and active on the server, ``False`` otherwise.
      :rtype: bool

   .. py:method:: isRemote()

      :return: ``True`` if the player is connected remotely (via network), ``False`` otherwise (e.g., local player, AI).
      :rtype: bool

   .. py:method:: isAIPlayer()

      :return: ``True`` if this player is an AI-controlled bot, ``False`` otherwise.
      :rtype: bool

   .. py:method:: isAlive()

      :return: ``True`` if the player's character is currently alive, ``False`` otherwise.
      :rtype: bool

   .. py:method:: isManDown()

      :return: ``True`` if the player is in a downed state (can be revived), ``False`` otherwise.
      :rtype: bool

   .. py:method:: isConnected()

      :return: ``True`` if the player is currently connected to the server, ``False`` otherwise.
      :rtype: bool

   .. py:method:: getProfileId()

      :return: The unique identifier for the player's profile.
      :rtype: int

   .. py:method:: isFlagHolder()

      :return: ``True`` if the player is currently holding a flag objective, ``False`` otherwise.
      :rtype: bool

   .. py:method:: getTeam()

      :return: The numerical ID of the team the player belongs to (e.g., 1 for Blufor, 2 for Opfor).
      :rtype: int

   .. py:method:: setTeam(t)

      :param t: The team ID to set the player to.
      :type t: int
      :return: None. Sets the player's team.
      :rtype: None

   .. py:method:: getPing()

      :return: The player's ping (network transit time from player to server and back) in milliseconds.
      :rtype: int

   .. py:method:: getSuicide()

      :return: ``1`` if the player has committed suicide (this resets once the player respawns), ``0`` otherwise.
      :rtype: int

   .. py:method:: setSuicide(t)

      :param t: Likely a value to indicate suicide state, exact usage may vary.
      :type t: int

   .. py:method:: getTimeToSpawn()

      :return: The number of seconds remaining until the player is allowed to spawn. Returns ``0`` if the player is already spawned in or is waiting to spawn.
      :rtype: int

   .. py:method:: setTimeToSpawn(t)

      This method appears to raise an exception if used on a player who is already spawned. If used on a player waiting to spawn, it changes the remaining time until they are allowed to spawn.

      :type t: int

   .. py:method:: getSquadId()

      Squads are numbered independently for each team, starting from ``1``. Players not assigned to a squad, including team commanders, are given squad ID ``0``.

      :return: The player's squad ID.
      :rtype: int

   .. py:method:: isSquadLeader()

      :return: ``True`` if player is a squad leader, ``False`` otherwise.
      :rtype: bool

   .. py:method:: isCommander()

      :return: ``True`` if player is currently the commander, ``False`` otherwise.
      :rtype: bool

   .. py:method:: getName()

      :return: Player's name.
      :rtype: str

   .. py:method:: setName(name)

      Sets a player's name (this changes the value returned by ``getName()``), but the change is not visible in-game to players already connected. Only players who connect *after* the name change will see the new name.

      :type name: str

   .. py:method:: getSpawnGroup()

      :return: Identifier for the spawn group the player is currently associated with.
      :rtype: int

   .. py:method:: setSpawnGroup(t)

      :param t: The spawn group ID to assign the player to.
      :type t: int

   .. py:method:: getKit()

      :return: The current player's kit object, or ``None`` if not applicable.
      :rtype: kitObject

   .. py:method:: getVehicle()

      :return: The current vehicle object the player is occupying, or their soldier object if they are not currently in a vehicle.
      :rtype: Any

   .. py:method:: getDefaultVehicle()

      :return: The player's soldier object, no matter what vehicle they are in.
      :rtype: soldierObject

   .. py:method:: getPrimaryWeapon()

      :return: The weapon object for the player's currently selected weapon.
      :rtype: weaponObject

   .. py:method:: getAddress()

      :return: The player's IP address as a string.
      :rtype: str

   .. py:method:: setIsInsideCP(value)

      :param value: Boolean value indicating if the player is inside a control point.
      :type value: bool

   .. py:method:: getIsInsideCP()

      :return: ``True`` if the player is inside a control point, ``False`` otherwise.
      :rtype: bool

   .. py:class:: score

      This object is instantiated as :py:class:`score`. Objects of this class store a comprehensive list of player score attributes. Each :py:class:`player` object (e.g., ``x``) has an associated :py:class:`score` object accessible via ``x.score``.

      You typically won't create :py:class:`score` objects directly; they are automatically generated as part of :py:class:`player` object creation. No special imports are needed to access their methods and attributes.

      There is also a separate ``player.stats`` object, which tracks different information. You can use the following code fragment to see all of the variables in the ``player.stats`` object.

      .. code-block:: python

         for s in vars(player.stats):
         print str(s)

      .. py:method:: reset()

         Resets all score attributes stored within the object itself to their default values.

         :rtype: None

      .. py:attribute:: index

         :type: int
         :description: The player's index.

      .. py:attribute:: heals

         :type: int
         :description: Score awarded for healing teammates.

      .. py:attribute:: ammos

         :type: int
         :description: Score awarded for resupplying teammates with ammunition.

      .. py:attribute:: repairs

         :type: int
         :description: Score awarded for repairing friendly vehicles.

      .. py:attribute:: damageAssists

         :type: int
         :description: Score awarded for assisting in damaging enemy targets.

      .. py:attribute:: passengerAssists

         :type: int
         :description: Score awarded for assisting as a passenger in a vehicle (e.g., gunner assists).

      .. py:attribute:: driverAssists

         :type: int
         :description: Score awarded for assisting as a driver of a vehicle (e.g., transporting squad members, enabling passengers to score).

      .. py:attribute:: targetAssists

         :type: int
         :description: Score awarded for assisting in targeting enemies, potentially through spotting or marking.

      .. py:attribute:: driverSpecials

         :type: int
         :description: Score awarded for special driver actions, such as ramming or specific vehicle objectives.

      .. py:attribute:: revives

         :type: int
         :description: Score awarded for reviving downed teammates.

      .. py:attribute:: teamDamages

         :type: int
         :description: Score penalty for dealing damage to teammates.

      .. py:attribute:: teamVehicleDamages

         :type: int
         :description: Score penalty for dealing damage to friendly vehicles.

      .. py:attribute:: cpCaptures

         :type: int
         :description: Score awarded for capturing control points.

      .. py:attribute:: cpDefends

         :type: int
         :description: Score awarded for defending control points.

      .. py:attribute:: cpAssists

         :type: int
         :description: Score awarded for assisting in control point captures or defends.

      .. py:attribute:: suicides

         :type: int
         :description: Score penalty for committing suicide.

      .. py:attribute:: cpNeutralizes

         :type: int
         :description: Score awarded for neutralizing enemy control points.

      .. py:attribute:: cpNeutralizeAssists

         :type: int
         :description: Score awarded for assisting in neutralizing control points.

      .. py:attribute:: rplScore

         :type: int
         :description: Possibly related to teamwork score or assists; may not be present in all BF2 versions.

      .. py:attribute:: skillScore

         :type: int
         :description: Score reflecting the player's overall skill, potentially derived from combat performance.

      .. py:attribute:: cmdScore

         :type: int
         :description: Score related to commander actions and performance.

      Class attributes stored in the BF2 engine:

      .. object:: deaths

         Total number of times the player has died.

         :type: int

      .. object:: kills

         Total number of enemies killed by the player.

         :type: int

      .. object:: TKs

         Total number of teamkills committed by the player.

         :type: int

      .. object:: score

         The player's current total score.

         :type: int

      .. object:: fracScore

         Fractional score, possibly used for score normalization or intermediate calculations.

         :type: float

      .. object:: rank

         The player's current rank or level.

         :type: int

      .. object:: firstPlace

         Number of times the player achieved first place in a round.

         :type: int

      .. object:: secondPlace

         Number of times the player achieved second place in a round.

         :type: int

      .. object:: thirdPlace

         Number of times the player achieved third place in a round.

         :type: int

      .. object:: bulletsFired

         Returns a tuple where each element is a 2-tuple containing the name of a weapon the player has fired and the number of shots fired from that weapon. As the player uses more weapons, more 2-tuples are added to the list. For example: ``(("uspi-m16", 30), ("knife", 3))``. Before the first weapon is fired, this might be ``None`` or an empty tuple. The first weapon fired isn't necessarily the first 2-tuple in the returned list.

         :type: tuple

      .. object:: bulletsGivingDamage

         Same as ``bulletsFired``, but only includes bullets that dealt damage.

         :type: tuple

      .. object:: bulletsFiredAndClear

         This attribute resets the engine counter after polling, so it only provides new bullet data. However, it's not recommended for multiple modules to poll this simultaneously.

         :type: tuple

      .. object:: bulletsGivingDamageAndClear

         Similar to ``bulletsFiredAndClear``, but for bullets that dealt damage.

         :type: tuple

      .. object:: dkRatio

         Likely represents the Kill/Death ratio.

         :type: float

.. py:class:: physicalObject

   :py:class:`physicalObject` instances represent tangible entities within the BF2 game world, possessing real-world properties like position (X, Y, Z coordinates) and orientation (rotation). They can also contain or be contained by other :py:class:`physicalObject` objects. These objects are implemented as C++ objects within the game engine, accessible to the embedded Python engine. They cannot be created directly in Python but can be manipulated from Python. No special imports are required to work with these objects.

   It's important to note that since these are not native Python objects, their exact names within the game engine are unknown. :py:class:`physicalObject` and its inheriting classes are named for convenience in this documentation. While the hierarchical structure presented here (e.g., :py:class:`vehicleObject` and :py:class:`soldierObject` being distinct) might differ from the internal game engine implementation (they could, for instance, be a single class), this documented hierarchy is conceptually equivalent to the real one.

   .. py:attribute:: templateName

      The name of the template that this object is based on.

      :type: str

   .. py:attribute:: isControlPoint

      Indicates whether this physical object represents a control point on the map.

      :type: bool

   .. py:attribute:: isPlayerControlObject

      Indicates whether this physical object can be controlled by a player (e.g., vehicles, turrets).

      :type: int

   .. py:attribute:: hasArmor

      Indicates whether this physical object possesses armor, affecting its durability.

      :type: bool

   .. py:attribute:: token

      An internal token or identifier for the object, possibly used for uniqueness or reference.

   .. py:method:: isValid()

      :return: ``1`` if the physical object is currently valid and active in the game world, ``0`` otherwise.
      :rtype: int

   .. py:method:: getTemplateProperty()

      :param parameter: The name of the template property to retrieve.
      :type parameter: str
      :return: The value of the specified template property.

      The known properties available via the ``getTemplateProperty`` method are:

      .. py:attribute:: radius

         For control points only. Represents the capture radius of the control point.

      .. py:attribute:: ControlPointID

         For control points only. The unique identifier of the control point.

   .. py:method:: getPosition()

      :return: A tuple (X, Y, Z) representing the object's position in world coordinates.
      :rtype: tuple

   .. py:method:: setPosition((X, Y, Z))

      :param position: A tuple (X, Y, Z) representing the new position in world coordinates.
      :type position: tuple
      :return: None. Sets the object's position.
      :rtype: None

   .. py:method:: getRotation()

      :return: A tuple (A, B, C) representing the object's rotation in degrees around the X, Y, and Z axes.
      :rtype: tuple

   .. py:method:: setRotation((A, B, C))

      :param rotation: A tuple (A, B, C) representing the new rotation in degrees around the X, Y, and Z axes.
      :type rotation: tuple
      :return: None. Sets the object's rotation.
      :rtype: None

   .. py:method:: getParent()

      :return: :py:class:`physicalObject` that contains this instance, if any. Returns ``None`` if the object is a root object.
      :rtype: PhysicalObject

   .. py:method:: getChildren()

      :return: A tuple of multiple :py:class:`physicalObject` instances that are children of this object. Returns an empty tuple if the object has no children.
      :rtype: tuple

   For information about the coordinate system used by the Position and Rotation methods, see the page on :doc:`BF2 Coordinates <../../engine/coordinates>`.

.. py:class:: weaponObject

   A :py:class:`weaponObject` represents a weapon in the game. This class inherits all methods and attributes from :py:class:`physicalObject`, with no additional methods or attributes of its own.

.. py:class:: kitObject

   A :py:class:`kitObject` represents a "kit" in the game. This class inherits all methods and attributes from :py:class:`physicalObject`, with no additional methods or attributes of its own.

.. py:class:: controlPointObject

   A :py:class:`controlPointObject` represents a control point in the game. This class inherits all methods and attributes from :py:class:`physicalObject`, and includes the following additional methods and attributes:

   .. py:attribute:: flagPosition

      Indicates the vertical position of the flag: ``0`` (top), ``1`` (middle), ``2`` (bottom).

      :type: int

   .. py:attribute:: lastAttackingTeam

      Stores the ID of the last team that attacked this control point.

      :type: int

   .. py:attribute:: triggerId

      An identifier for the trigger associated with this control point, likely used for area-based events.

      :type: int

   .. py:method:: cp_getParam(parameter)

      :param parameter: The name of the parameter to retrieve.
      :type parameter: str
      :return: The value of the specified control point parameter.
      :rtype: Any

   .. py:method:: cp_setParam(parameter, value)

      :param parameter: The name of the parameter to set.
      :type parameter: str
      :param value: The value to set for the parameter.
      :type value: Any
      :return: None. Sets a control point parameter.
      :rtype: None

   :py:class:`controlPointObject` also have a number of internal properties that are accessed through the :py:meth:`cp_getParam` and :py:meth:`cp_setParam` methods:

   .. py:property:: isHemisphere

      :type: bool
      :description: A value of ``True`` or ``False`` indicating whether the control point's capture area is hemispherical.

   .. py:property:: team

      :type: int
      :description: The team that currently owns the capture point: ``0`` for neutral, ``1`` for team 1, and ``2`` for team 2. Changing this value also updates the minimap and flag tag indicator.

   .. py:property:: flag

      :type: int
      :description: The image identifier used for the control point's flag: ``1`` for team 1's flag, ``2`` for team 2's.

   .. py:property:: areaValue

      :type: int
      :description: The weighting value for this control point, potentially affecting capture speed or ticket bleed.

   .. py:property:: unableToChangeTeam

      :type: int
      :description: Indicates whether this control point is capturable (``0``) or not (``1``). A value of ``1`` might mean it's locked or impassable.

   .. py:property:: timeToGetControl

      :description: The number of seconds it takes to capture this control point under normal conditions.

   .. py:property:: timeToLoseControl

      :description: The number of seconds it takes to lose control of this control point.

   .. py:property:: onlyTakeableByTeam

      :type: str
      :description: Indicates whether this control point can only be captured by one specific team (``1``) or not (``0``).

   .. py:property:: takeOverChangePerSecond

      :type: int
      :description: The speed at which the flag at this control point is captured or lost, measured in percentage change per second.

   .. py:property:: enemyTicketLossWhenCaptured

      :type: int
      :description: The number of tickets lost by the enemy team when this control point is captured (needs verification).

   .. py:property:: playerId

      :type: int
      :description: Purpose unknown; possibly sets the ``playerID`` of the first player to capture this control point (the initial capturer, not assisting players).

.. py:class:: vehicleObject

   A :py:class:`vehicleObject` represents a vehicle in BF2. This class inherits all methods and attributes from :py:class:`PhysicalObject`, and includes several additional methods. The :py:class:`soldierObject`, which represents a player's physical body, is a subclass of :py:class:`vehicleObject`.

   .. py:method:: getDamage()

      :return: The current damage value of the vehicle, likely as a float or int.
      :rtype: float

   .. py:method:: setDamage(intValue)

      :param intValue: The new damage value to set for the vehicle.
      :type intValue: int
      :return: None. Sets the vehicle's damage state.
      :rtype: None

   .. py:method:: getIsWreck()

      :return: ``1`` if the vehicle is destroyed and in a wrecked state, ``0`` otherwise.
      :rtype: int

   .. py:method:: getOccupyingPlayers()

      :return: An array (or list) of player objects currently occupying the vehicle. The index ``0`` typically represents the driver.
      :rtype: list

   .. py:method:: getIsRemoteControlled()

      :return: ``True`` if the vehicle is currently remote-controlled (e.g., by commander abilities or AI), ``False`` otherwise.
      :rtype: bool

   The :py:meth:`getDamage` and :py:meth:`setDamage` methods control the vehicle's health. For example, transport helicopters start with 1500 health, tanks with 1000, and light jeeps with 750. All vehicles explode when their health reaches 0.

.. py:class:: soldierObject

   A :py:class:`soldierObject` represents the physical body of a human or AI player in the game. This class inherits all methods and attributes from :py:class:`vehicleObject`, with no additional methods or attributes of its own. (Note: It appears that within the game engine, :py:class:`soldierObject` and :py:class:`vehicleObject` might be the same entity; however, it's conceptually helpful to consider :py:class:`soldierObject` as a subclass of :py:class:`vehicleObject`).

   It's crucial to distinguish between a player's "physical" body in the game, represented by a :py:class:`soldierObject` instance (with properties like position, orientation, health), and the player's in-game "spirit," represented by a :py:class:`player` instance (with properties like name, squad, profile ID). The :py:class:`player` ("spirit") is created when a player connects to the server and persists across game rounds, even if the player disconnects and reconnects (the server attempts to re-link them with an existing :py:class:`player` object). In contrast, a player is associated with a :py:class:`soldierObject` only while they are alive. Upon death, this association breaks, and a new :py:class:`soldierObject` instance is created and linked to the player when they respawn. Essentially, between dying and respawning, the player's "spirit" leaves its initial "body" and is "reincarnated" into a new one.
