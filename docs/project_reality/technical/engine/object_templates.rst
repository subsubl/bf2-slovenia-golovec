
Game Engine Object Templates
============================

This is a list of C++ game engine "object types" that can be used in the :py:meth:`bf2.ObjectManager.getObjectsOfType` method. As an example, to get a list of all control points, you could use: :py:meth:`PhysicalObject.getChildren`

.. code-block:: python

   controlPoints = bf2.objectManager.getObjectsOfType('dice.hfe.world.ObjectTemplate.ControlPoint')
   for cp in controlPoints:
      # do stuff to each control point``

Confirmed ObjectTemplates
-------------------------

.. list-table::
   :header-rows: 1

   * - ObjectType
     - Parent
     - Children
   * - ``dice.hfe.world.ObjectTemplate.PlayerControlObject``
     - None
     - None
   * - ``dice.hfe.world.ObjectTemplate.ControlPoint``
     - None
     - Type :py:class:`PhysicalObject` (flagpole, flag_us, flag_mec, flag_ch, flag_neutral)
   * - ``dice.hfe.world.ObjectTemplate.Trigger``
     - None
     - None
   * - ``dice.hfe.world.ObjectTemplate.AmbientEffectArea``
     - None
     - None
   * - ``dice.hfe.world.ObjectTemplate.Ladder``
     - None
     - None
   * - ``dice.hfe.world.ObjectTemplate.TargetObject``
     - None
     - None
   * - ``dice.hfe.world.ObjectTemplate.ObjectSpawner``
     - None
     - Mixed type depending on the type of the parent object.
   * - ``dice.hfe.world.ObjectTemplate.Soldier``
     - None
     - Unknown type
   * - ``dice.hfe.world.ObjectTemplate.AnimatedBundle``
     - None
     - None
   * - ``dice.hfe.world.ObjectTemplate.Kit``
     - None
     - Unknown type
   * - ``dice.hfe.world.ObjectTemplate.DestroyableObject``
     - None
     - None

Detailed ObjectTemplate Descriptions
------------------------------------

``dice.hfe.world.ObjectTemplate.PlayerControlObject``
   Returns a tuple of vehicle-like objects a player can control (including Commander assets). Vehicles are made of many objects; use :py:class:`getChildren() <PhysicalObject.getChildren>` to get all objects in a vehicle.

``dice.hfe.world.ObjectTemplate.ControlPoint``
   Returns a tuple of :py:class:`ControlPoint objects <controlPointObject>`. A control point consists of a flagpole and a flag. The flag image changes based on which team controls the point.

``dice.hfe.world.ObjectTemplate.Trigger``
   Returns a tuple of unknown object types.

``dice.hfe.world.ObjectTemplate.AmbientEffectArea``
   Returns a tuple of unknown object types.

``dice.hfe.world.ObjectTemplate.Ladder``
   Returns a tuple of unknown object types.

``dice.hfe.world.ObjectTemplate.TargetObject``
   Returns a tuple of unknown object types, seemingly always `UniqueTarget`. The first two objects usually represent artillery: the first for MEC or China, the second for US. At the start of a round, all TargetObjects are at (0.0, 0.0, 0.0). When artillery fires, its TargetObject's position updates to the artillery's location and stays there until the next shot. Other objects in the tuple are for guided missiles (e.g., TV-Guided Missiles) in the level.

``dice.hfe.world.ObjectTemplate.ObjectSpawner``
   Returns a tuple of :py:class:`PhysicalObject objects <PhysicalObject>`. Spawned objects are defined in the :file:`GamePlayObjects.con` file within server.zip (`GameModes//`). Examples include UAVs, JEEP_AAVs, and destroyable bridges.

``dice.hfe.world.ObjectTemplate.Soldier``
   Returns a tuple of unknown object types.

``dice.hfe.world.ObjectTemplate.AnimatedBundle``
   Returns a tuple of unknown object types.

``dice.hfe.world.ObjectTemplate.Kit``
   Returns a tuple of unknown object types.

``dice.hfe.world.ObjectTemplate.DestroyableObject``
   Returns a tuple of unknown object types.

Unconfirmed ObjectTemplates
---------------------------

These objects are valid but return an empty tuple. They are probably not accessible from python, or only valid when these objects exist in the map. This is not tested. Any insight on these objects is highly appreciated.

- ``dice.hfe.world.TemplateComponent.PreDestinedFollowComp``
- ``dice.hfe.world.TemplateComponent.DefaultFollowComp``
- ``dice.hfe.world.TemplateComponent.FixedTargetComp``
- ``dice.hfe.world.TemplateComponent.SeekClosestTargetComp``
- ``dice.hfe.world.TemplateComponent.DefaultRicochetComp``
- ``dice.hfe.world.TemplateComponent.DefaultPenetrateComp``
- ``dice.hfe.world.TemplateComponent.DefaultProjSoundComp``
- ``dice.hfe.world.TemplateComponent.ReplenishDetonationComp``
- ``dice.hfe.world.TemplateComponent.DefaultDetonationComp``
- ``dice.hfe.world.TemplateComponent.StickyCollisionComp``
- ``dice.hfe.world.TemplateComponent.ResurrectCollisionComp``
- ``dice.hfe.world.TemplateComponent.ReplenishCollisionComp``
- ``dice.hfe.world.TemplateComponent.DefaultCollisionComp``
- ``dice.hfe.world.TemplateComponent.ExplosivesFireComp``
- ``dice.hfe.world.TemplateComponent.ThrownFireComp``
- ``dice.hfe.world.TemplateComponent.SpawnObjectFireComp``
- ``dice.hfe.world.TemplateComponent.LPFireComp``
- ``dice.hfe.world.TemplateComponent.SimpleTargetComp``
- ``dice.hfe.world.TemplateComponent.LPTargetComp``
- ``dice.hfe.world.TemplateComponent.MultiFireArmTargetComp``
- ``dice.hfe.world.TemplateComponent.ThrownAnimationComp``
- ``dice.hfe.world.TemplateComponent.DefaultAnimationComp``
- ``dice.hfe.world.TemplateComponent.TargetDeviationComp``
- ``dice.hfe.world.TemplateComponent.SimpleDeviationComp``
- ``dice.hfe.world.TemplateComponent.SoldierDeviationComp``
- ``dice.hfe.world.TemplateComponent.WeaponBasedRecoilComp``
- ``dice.hfe.world.TemplateComponent.SoldierBasedRecoilComp``
- ``dice.hfe.world.TemplateComponent.DefaultSoundComp``
- ``dice.hfe.world.TemplateComponent.ToggleCameraComp``
- ``dice.hfe.world.TemplateComponent.DefaultZoomComp``
- ``dice.hfe.world.TemplateComponent.ReplenishingAmmoComp``
- ``dice.hfe.world.TemplateComponent.DefaultAmmoComp``
- ``dice.hfe.world.TemplateComponent.MultiFireComp``
- ``dice.hfe.world.TemplateComponent.SingleFireComp``
- ``dice.hfe.world.TemplateComponent.StrategicObject``
- ``dice.hfe.world.TemplateComponent.HelpHud``
- ``dice.hfe.world.TemplateComponent.WarningHud``
- ``dice.hfe.world.TemplateComponent.AbilityHud``
- ``dice.hfe.world.TemplateComponent.WeaponHud``
- ``dice.hfe.world.TemplateComponent.VehicleHud``
- ``dice.hfe.world.TemplateComponent.PostProcess``
- ``dice.hfe.world.ObjectTemplate.GenericProjectile``
- ``dice.hfe.world.ObjectTemplate.TurnableRemoteControlledObject``
- ``dice.hfe.world.ObjectTemplate.RemoteControlledObject``
- ``dice.hfe.world.ObjectTemplate.LadderContainer``
- ``dice.hfe.world.ObjectTemplate.AreaObject``
- ``dice.hfe.world.ObjectTemplate.Obstacle``
- ``dice.hfe.world.ObjectTemplate.SupplyObject``
- ``dice.hfe.world.ObjectTemplate.SupplyDepot``
- ``dice.hfe.world.ObjectTemplate.KitPart``
- ``dice.hfe.world.ObjectTemplate.Parachute``
- ``dice.hfe.world.ObjectTemplate.GenericFireArm``
- ``dice.hfe.world.ObjectTemplate.AntennaObject``
- ``dice.hfe.world.ObjectTemplate.DestroyableWindow``
- ``dice.hfe.world.ObjectTemplate.DestroyableWindowsBundle``
- ``dice.hfe.world.ObjectTemplate.ItemContainer``
- ``dice.hfe.world.ObjectTemplate.Item``
