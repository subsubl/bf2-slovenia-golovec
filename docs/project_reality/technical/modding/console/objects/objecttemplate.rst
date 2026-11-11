
objectTemplate
==============

.. object:: objectTemplate.3dMapIcon <int>

   :returns: int

   - Used in GenericFirearms (Mine etc) .tweak
   - The image number sequence referenced in :file:`Objects.dds`.
   - Use the vBF2 file and count the images. 9 is the mine icon.
   - Using this system, you could have custom 3D Mine Icons, as long as they are the same size as the original.

.. object:: objectTemplate.ability.hasAmmoAbility <bool>

   :returns: bool

.. object:: objectTemplate.ability.hasHealingAbility <bool>

   :returns: bool

.. object:: objectTemplate.ability.hasRepairingAbility <bool>

   :returns: bool

.. object:: objectTemplate.ability.radarRadius <int>

   :returns: int

.. object:: objectTemplate.abilityHud.ammoSound <std::string>

   :returns: std::string

.. object:: objectTemplate.abilityHud.healingSound <std::string>

   :returns: std::string

.. object:: objectTemplate.abilityHud.repairingSound <std::string>

   :returns: std::string

.. object:: objectTemplate.abilityInVehicleMaterial <int>

   :returns: int

.. object:: objectTemplate.abilityInVehicleRadius <float>

   :returns: float

.. object:: objectTemplate.abilityInVehicleStrength <float>

   :returns: float

.. object:: objectTemplate.abilityRestoreRate <float>

   :returns: float

.. object:: objectTemplate.acceleration <Math::Vec3>

   :returns: Math::Vec3

.. object:: objectTemplate.acceleration <float>

   :returns: float

.. object:: objectTemplate.accumulate <bool>

   :returns: bool

.. object:: ObjectTemplate.active <world::IObjectTemplate_ptrproxy>

   :returns: world::IObjectTemplate_ptrproxy

.. object:: ObjectTemplate.activeSafe <std::string world::IObjectTemplate_ptrproxy>

   :returns: void

.. object:: objectTemplate.addAmmoType <int int float>

   :returns: void

.. object:: objectTemplate.addChild <bool>

   :returns: bool

.. object:: objectTemplate.addEmitterSpeed <bool>

   :returns: bool

.. object:: objectTemplate.addKitVehicleMod <std::string int>

   :returns: void

.. object:: objectTemplate.addLinePoint <Vec2>

   :returns: void

.. object:: objectTemplate.addPcoPosId <int>

   :returns: void

.. object:: objectTemplate.addTargetObjectTypeToWatch <int>

   :returns: void

.. object:: objectTemplate.addTemplate <std::string>

   :returns: void

.. object:: objectTemplate.addToCollisionGroup <U32>

   :returns: void

.. object:: objectTemplate.addToProjectileList <bool>

   :returns: bool

.. object:: objectTemplate.addTriggerableTarget <std::string>

   :returns: void

.. object:: objectTemplate.addVehicleType <std::string int float>

   :returns: void

.. object:: objectTemplate.addVehicleType <VehicleCategory>

   :returns: void

.. object:: objectTemplate.addWorkOnMaterial <int>

   :returns: void

.. object:: objectTemplate.affectingType <int>

   :returns: int

.. object:: objectTemplate.affectLightmappedObjects <bool>

   :returns: bool

.. object:: objectTemplate.AgeScaleFactorFromAcceleration <Vec2>

   :returns: Vec2

.. object:: objectTemplate.AgeScaleFactorFromAltitude <Vec2>

   :returns: Vec2

.. object:: objectTemplate.AgeScaleFactorFromEngine <Vec2>

   :returns: Vec2

.. object:: objectTemplate.AgeScaleFactorFromRotationalSpeed <Vec2>

   :returns: Vec2

.. object:: objectTemplate.AgeScaleFactorFromSpeed <Vec2>

   :returns: Vec2

.. object:: objectTemplate.AgeScaleFactorFromSpeedInDof <Vec2>

   :returns: Vec2

.. object:: objectTemplate.AgeScaleFactorRange <Vec2>

   :returns: Vec2

.. object:: objectTemplate.AgeScaleFactorUsed <bool>

   :returns: bool

.. object:: objectTemplate.airFlowAffect <float>

   :returns: float

.. object:: objectTemplate.airFriction <float>

   :returns: float

.. object:: objectTemplate.airResistance <float>

   :returns: float

.. object:: objectTemplate.airResistanceGraph <Vec4>

   :returns: Vec4

.. object:: objectTemplate.aiTemplate <std::string>

   :returns: std::string

.. object:: objectTemplate.alignEffectTransformation <bool>

   :returns: bool

.. object:: objectTemplate.alignRotationToSpeed <bool>

   :returns: bool

.. object:: objectTemplate.allowDucking <bool>

   :returns: bool

.. object:: objectTemplate.allowInsideDynamicLights <bool>

   :returns: bool

.. object:: objectTemplate.allowInsideStaticSun <bool>

   :returns: bool

.. object:: objectTemplate.alphaCull <float>

   :returns: float

.. object:: objectTemplate.alphaIntensityFromAcceleration <Vec2>

   :returns: Vec2

.. object:: objectTemplate.alphaIntensityFromAltitude <Vec2>

   :returns: Vec2

.. object:: objectTemplate.alphaIntensityFromEngine <Vec2>

   :returns: Vec2

.. object:: objectTemplate.alphaIntensityFromRotationalSpeed <Vec2>

   :returns: Vec2

.. object:: objectTemplate.alphaIntensityFromSpeed <Vec2>

   :returns: Vec2

.. object:: objectTemplate.alphaIntensityFromSpeedInDof <Vec2>

   :returns: Vec2

.. object:: objectTemplate.alphaIntensityRange <Vec2>

   :returns: Vec2

.. object:: objectTemplate.alphaIntensityUsed <bool>

   :returns: bool

.. object:: objectTemplate.alphaOverTime <OverTimeDistribution>

   :returns: OverTimeDistribution

.. object:: objectTemplate.alternateTemplate0 <std::string>

   :returns: std::string

.. object:: objectTemplate.alternateTemplate1 <std::string>

   :returns: std::string

.. object:: objectTemplate.alternateTemplate2 <std::string>

   :returns: std::string

.. object:: objectTemplate.alternateTemplate3 <std::string>

   :returns: std::string

.. object:: objectTemplate.alternateTemplate4 <std::string>

   :returns: std::string

.. object:: objectTemplate.altSoldierExitPosition <Vec3>

   :returns: Vec3

.. object:: objectTemplate.ammo.abilityCost <float>

   :returns: float

.. object:: objectTemplate.ammo.abilityDrain <float>

   :returns: float

.. object:: objectTemplate.ammo.abilityMaterial <int>

   :returns: int

.. object:: objectTemplate.ammo.abilityRadius <float>

   :returns: float

.. object:: objectTemplate.ammo.abilityStrength <float>

   :returns: float

.. object:: objectTemplate.ammo.ammoType <int>

   :returns: int

.. object:: objectTemplate.ammo.autoReload <bool>

   :returns: bool

.. object:: objectTemplate.ammo.changeMagAt <float>

   :returns: float

.. object:: objectTemplate.ammo.firstShotExtraTime <float>

   :returns: float

.. object:: objectTemplate.ammo.instantReloadOnEnable <bool>

   :returns: bool

.. object:: objectTemplate.ammo.lastShotExtraTime <float>

   :returns: float

.. object:: objectTemplate.ammo.magLinkWeapon <std::string>

   :returns: std::string

   - Weapons, Vehicles :file:`.tweak`
   - Allows two weapons to share the same amount of bullets and magazines.
   - Enter the weapon name to maglink.
   - The weapon that's referenced must also have the same code.
   - Weapons with fire selector code causes it to not work properly (citation needed)

.. object:: objectTemplate.ammo.magSize <int>

   :returns: int

   - Weapons :file:`.tweak`
   - Number of bullets in a magazine.

     - -1 for Infinity
     - Maximum non-infinity allowed is 1023
     - Any more will cause a crash

   .. error::

      In the Battlerecorder, it doesn't pickup a gun that fires for 10 seconds on with 1000 bullets for some reason. Tested with the L4Bren on Auto.

.. object:: objectTemplate.ammo.minimumTimeUntilReload <float>

   :returns: float

.. object:: objectTemplate.ammo.nrOfMags <int>

   :returns: int

   Number of magazines allowed for a weapon.

.. object:: objectTemplate.ammo.onlyActiveWhileFiring <bool>

   :returns: bool

   Prevents the Medibag and Ammo Bag from being thrown when firing. Used in PR's Medikit and Repair Bag

.. object:: objectTemplate.ammo.reloadAmount <int>

   :returns: int

.. object:: objectTemplate.ammo.reloadTime <float>

   :returns: float

   - Time in seconds of how long it takes to reload.
   - Must be the same number as the reload animation time from AnimationSystem1p.inc to sync properly.

.. object:: objectTemplate.ammo.reloadWithoutPlayer <bool>

   :returns: bool

   - If enabled, weapon will autoreload regardless client settings for autoreload.
   - 1 - Enabled
   - 0 - Disabled

.. object:: objectTemplate.ammo.replenishingType <ReplenishingType>

   :returns: ReplenishingType

.. object:: objectTemplate.ammo.toggleWhenNoAmmo <bool>

   :returns: bool

   - Weapons :file:`.tweak`
   - When no ammo, switch to previous selected weapon.

.. object:: objectTemplate.ammoStorageSize <float>

   :returns: float

.. object:: objectTemplate.anchor <Vec3>

   :returns: Vec3

.. object:: objectTemplate.anchorOffset <Vec3>

   :returns: Vec3

.. object:: objectTemplate.animatedUVRotation <int>

   :returns: int

.. object:: objectTemplate.animatedUVRotationIndex <int>

   :returns: int

.. object:: objectTemplate.animatedUVRotationRadius <float>

   :returns: float

.. object:: objectTemplate.animatedUVRotationReverse <bool>

   :returns: bool

.. object:: objectTemplate.animatedUVRotationScale <Vec2>

   :returns: Vec2

.. object:: objectTemplate.animatedUVTranslation <bool>

   :returns: bool

.. object:: objectTemplate.animatedUVTranslationIndex <int>

   :returns: int

.. object:: objectTemplate.animatedUVTranslationMax <Vec2>

   :returns: Vec2

.. object:: objectTemplate.animatedUVTranslationReverse <bool>

   :returns: bool

.. object:: objectTemplate.animatedUVTranslationSize <Vec2>

   :returns: Vec2

.. object:: objectTemplate.animatedUVTranslationSpeed <Vec2>

   :returns: Vec2

.. object:: objectTemplate.animation.animateOnZoom <bool>

   :returns: bool

.. object:: objectTemplate.animation.loopingFire <float>

   :returns: float

.. object:: objectTemplate.animation.shiftDelay <float>

   :returns: float

.. object:: objectTemplate.animation.useShiftAnimation <bool>

   :returns: bool

.. object:: objectTemplate.animationEnable <bool>

   :returns: bool

.. object:: objectTemplate.animationFrameCount <int>

   :returns: int

.. object:: objectTemplate.animationFrameCountX <int>

   :returns: int

.. object:: objectTemplate.animationFrameHeight <int>

   :returns: int

.. object:: objectTemplate.animationFrameWidth <int>

   :returns: int

.. object:: objectTemplate.animationPlayOnce <bool>

   :returns: bool

.. object:: objectTemplate.animationRandomizedStartFrame <bool>

   :returns: bool

.. object:: objectTemplate.animationSpeed <float>

   :returns: float

.. object:: objectTemplate.animationSystem1P <std::string>

   :returns: void

.. object:: objectTemplate.animationSystem3P <std::string>

   :returns: void

.. object:: objectTemplate.antenna.accelerationFactor <float>

   :returns: float

.. object:: objectTemplate.antenna.damping <float>

   :returns: float

.. object:: objectTemplate.antenna.maxSwayAngle <Vec2>

   :returns: Vec2

.. object:: objectTemplate.antenna.skeleton <std::string>

   :returns: std::string

.. object:: objectTemplate.antenna.speedFactor <float>

   :returns: float

.. object:: objectTemplate.antenna.stiffness <float>

   :returns: float

.. object:: objectTemplate.areaValueTeam1 <U32>

   :returns: U32

.. object:: objectTemplate.areaValueTeam2 <U32>

   :returns: U32

.. object:: objectTemplate.armingDelay <float>

   :returns: float

   - Weapons :file:`.tweak`
   - Delay in seconds until the collision event is active.
   - Used in the tripflares, which has a 15 second delay before passing through it will trigger the collision.

     - Also could just be the seconds before the grenade explodes though not sure

.. object:: objectTemplate.armor.addArmorEffect <int std::string Vec3>

   :returns: void

.. object:: objectTemplate.armor.addArmorEffectSpectacular <int std::string Vec3>

   :returns: void

.. object:: objectTemplate.armor.addWreckArmorEffect <int std::string Vec3>

   :returns: void

.. object:: objectTemplate.armor.alignLastEffectToHitDirection <bool>

   :returns: bool

.. object:: objectTemplate.armor.angleMod <float>

   :returns: float

.. object:: objectTemplate.armor.attackDamage <float>

   :returns: float

.. object:: objectTemplate.armor.canBeDestroyed <bool>

   :returns: bool

.. object:: objectTemplate.armor.canBeRepairedWhenWreck <bool>

   :returns: bool

   - Vehicles .tweak, Weapons :file:`.tweak`
   - Used in the AA Ship Boats.
   - Basically, when it's a wreck, it can be repaired back to life.

.. object:: objectTemplate.armor.criticalDamage <float>

   :returns: float

.. object:: objectTemplate.armor.deepWaterDamageDelay <float>

   :returns: float

.. object:: objectTemplate.armor.deepWaterLevel <float>

   :returns: float

.. object:: objectTemplate.armor.defaultMaterial <int>

   :returns: int

.. object:: objectTemplate.armor.destroyOnSpectacularDeath <bool>

   :returns: bool

.. object:: objectTemplate.armor.explosionDamage <float>

   :returns: float

.. object:: objectTemplate.armor.explosionForce <float>

   :returns: float

.. object:: objectTemplate.armor.explosionForceMax <float>

   :returns: float

.. object:: objectTemplate.armor.explosionForceMod <float>

   :returns: float

.. object:: objectTemplate.armor.explosionMaterial <int>

   :returns: int

.. object:: objectTemplate.armor.explosionRadius <float>

   :returns: float

.. object:: objectTemplate.armor.hideChildrenOnSpectacularDeath <bool>

   :returns: bool

.. object:: objectTemplate.armor.hitPoints <float>

   :returns: float

   - Vehicles :file:`.tweak`
   - The health of the vehicle.
   - 0 - Dead.

.. object:: objectTemplate.armor.hpLostWhileCriticalDamage <float>

   :returns: float

.. object:: objectTemplate.armor.hpLostWhileInDeepWater <float>

   :returns: float

.. object:: objectTemplate.armor.hpLostWhileInWater <float>

   :returns: float

.. object:: objectTemplate.armor.hpLostWhileUpSideDown <float>

   :returns: float

.. object:: objectTemplate.armor.maxHitPoints <float>

   :returns: float

.. object:: objectTemplate.armor.showDamageAsDirt <float>

   :returns: float

.. object:: objectTemplate.armor.speedMod <float>

   :returns: float

.. object:: objectTemplate.armor.timeToStayAfterDestroyed <float>

   :returns: float

   - Vehicles :file:`.tweak`
   - Interesting code. If set to PR's Jets and Helis, when they explode from wreck, the non-flaming wreck model stays though it shows in the minimap as an occupied vehicle.

.. object:: objectTemplate.armor.timeToStayAsWreck <float>

   :returns: float

.. object:: objectTemplate.armor.useMMOnDeath <bool>

   :returns: bool

   - Use the Material Manager on Death. Not too sure about this one

.. object:: objectTemplate.armor.waterDamageDelay <float>

   :returns: float

.. object:: objectTemplate.armor.waterLevel <float>

   :returns: float

.. object:: objectTemplate.armor.wreckDelay <float>

   :returns: float

.. object:: objectTemplate.armor.wreckExplosionDamage <float>

   :returns: float

.. object:: objectTemplate.armor.wreckExplosionForce <float>

   :returns: float

.. object:: objectTemplate.armor.wreckExplosionForceMax <float>

   :returns: float

.. object:: objectTemplate.armor.wreckExplosionForceMod <float>

   :returns: float

.. object:: objectTemplate.armor.wreckExplosionMaterial <int>

   :returns: int

.. object:: objectTemplate.armor.wreckExplosionRadius <float>

   :returns: float

.. object:: objectTemplate.armor.wreckHitPoints <float>

   :returns: float

.. object:: objectTemplate.artPos <bool>

   :returns: bool

.. object:: objectTemplate.attachClimberRadius <float>

   :returns: float

.. object:: objectTemplate.attachToEventObject <bool>

   :returns: bool

.. object:: objectTemplate.attackSpeed <float>

   :returns: float

.. object:: objectTemplate.attenuationRange1 <float>

   :returns: float

   - Used in :file:`.tweak` Effect Files for Lightsource Templates
   - How wide you want the lightsource effect to be, used with ``ObjectTemplate.isDynamic 1``.
   - Range1 - X, which is the horizontal range.
   - Max is 100, more than that will trigger an error message

.. object:: objectTemplate.attenuationRange2 <float>

   :returns: float

   - Used in :file:`.tweak` Effect Files for Lightsource Templates
   - The height at which the lightsource will begin to drop.
   - Range2 - Y, which is the vertical range.
   - Max is 100, like above.

      To know the difference, set one to 50 and one to 100 and count the number of seconds the lightsource effect will last and compare.

.. object:: objectTemplate.audio.newStyleAudio <bool>

   :returns: bool

.. object:: objectTemplate.audio.transformationRelativeRoot <bool>

   :returns: bool

.. object:: objectTemplate.audioReset

   :returns: void

.. object:: objectTemplate.automaticPitchStabilization <bool>

   :returns: bool

.. object:: objectTemplate.automaticReset <bool>

   :returns: bool

.. object:: objectTemplate.automaticYawStabilization <bool>

   :returns: bool

.. object:: objectTemplate.autoUseAbility <int>

   :returns: int

.. object:: objectTemplate.averageTimeBetweenTests <float>

   :returns: float

.. object:: objectTemplate.awakeTime <float>

   :returns: float

.. object:: objectTemplate.blendMode <std::string>

   :returns: std::string

.. object:: objectTemplate.blockInputOnRotBundle <std::string>

   :returns: std::string

.. object:: objectTemplate.blurryVisionHoldTime <float>

   :returns: float

.. object:: objectTemplate.blurryVisionTime <float>

   :returns: float

.. object:: objectTemplate.boneName <std::string>

   :returns: std::string

.. object:: objectTemplate.bounceDamping <float>

   :returns: float

.. object:: objectTemplate.bounceLength <float>

   :returns: float

.. object:: objectTemplate.bounceSensitivity <float>

   :returns: float

.. object:: objectTemplate.bounceStrength <float>

   :returns: float

.. object:: objectTemplate.boundingRadiusModifierWhenOccupied <float>

   :returns: float

.. object:: objectTemplate.cameraId <int>

   :returns: int

.. object:: objectTemplate.cameraShakeMaxSpeed <float>

   :returns: float

.. object:: objectTemplate.cameraShakeSensitivity <float>

   :returns: float

.. object:: objectTemplate.cameraShakeStartSpeed <float>

   :returns: float

.. object:: objectTemplate.cameraSwayDofMax <float>

   :returns: float

.. object:: objectTemplate.cameraSwayDofMin <float>

   :returns: float

.. object:: objectTemplate.cameraSwayRightMax <float>

   :returns: float

.. object:: objectTemplate.cameraSwayRightMin <float>

   :returns: float

.. object:: objectTemplate.cameraSwayRodLength <float>

   :returns: float

.. object:: objectTemplate.cameraSwaySensitivity <float>

   :returns: float

.. object:: objectTemplate.cameraSwaySpringDamping <float>

   :returns: float

.. object:: objectTemplate.cameraSwaySpringStrength <float>

   :returns: float

.. object:: objectTemplate.canFireGuiIndex <int>

   :returns: int

.. object:: objectTemplate.cannotFireGuiIndex <int>

   :returns: int

.. object:: objectTemplate.cannotFireTimer <float>

   :returns: float

.. object:: objectTemplate.canPickup <bool>

   :returns: bool

   - Weapons
   - Allows explosives to be picked up using the wrench/repair object
   - Example: ``at_mine``

.. object:: objectTemplate.canReverse <bool>

   :returns: bool

.. object:: objectTemplate.capMaxSpeed <bool>

   :returns: bool

.. object:: objectTemplate.castsDynamicShadow <bool>

   :returns: bool

   - Vehicles, Weapons, and Soldiers
   - Enables the rendering of shadows.

.. object:: objectTemplate.castsStaticShadow <bool>

   :returns: bool

.. object:: objectTemplate.centerOfCollisionOffset <Vec3>

   :returns: Vec3

.. object:: objectTemplate.centerOfMassOffset <Vec3>

   :returns: Vec3

   To offset the center of mass using 0/0/0 - ``X/Y/Z.`` Setting it to X/0.5/Z will make a Logistics Truck survive a direct ram to a Van while setting to 0 makes the truck crash. Tested while holding shift.

.. object:: objectTemplate.chance <float>

   :returns: float

   - :file:`AmbientObjects.con`
   - Chance that the triggerable effect may play when the player steps inside the radius.

      :1: always play
      :0: never play

.. object:: objectTemplate.changeLodAt <float>

   :returns: float

.. object:: objectTemplate.chaseAngle <float>

   :returns: float

.. object:: objectTemplate.chaseDistance <float>

   :returns: float

.. object:: objectTemplate.chaseOffset <Vec3>

   :returns: Vec3

.. object:: objectTemplate.clearTemplateList

   :returns: void

.. object:: objectTemplate.clientHitDetection <bool>

   :returns: bool

.. object:: objectTemplate.climbableAngle <float>

   :returns: float

.. object:: objectTemplate.climbersAttachForce <float>

   :returns: float

.. object:: objectTemplate.climbingSpeed <float>

   :returns: float

.. object:: objectTemplate.clockwise <bool>

   :returns: bool

.. object:: objectTemplate.cockpitLod <int>

   :returns: int

.. object:: objectTemplate.cockpitLod <U32>

   :returns: U32

.. object:: objectTemplate.cockpitSubGeom <int>

   :returns: int

.. object:: objectTemplate.cockpitSubGeom <U32>

   :returns: U32

.. object:: objectTemplate.collision.bouncing <bool>

   :returns: bool

.. object:: objectTemplate.collision.hasCollisionEffect <bool>

   :returns: bool

.. object:: objectTemplate.collision.maxStickAngle <float>

   :returns: float

.. object:: objectTemplate.collision.replenishingStrength <float>

   :returns: float

.. object:: objectTemplate.collision.replenishingType <ReplenishingType>

   :returns: ReplenishingType

.. object:: objectTemplate.collision.restoreHP <float>

   :returns: float

.. object:: objectTemplate.collision.resurrectDamage <float>

   :returns: float

.. object:: objectTemplate.collision.stickToStaticObjects <bool>

   :returns: bool

.. object:: objectTemplate.collision.stickToTerrain <bool>

   :returns: bool

.. object:: objectTemplate.collision.stickToVehicles <bool>

   :returns: bool

.. object:: objectTemplate.collisionEffectName <std::string>

   :returns: std::string

.. object:: objectTemplate.collisionEnable <bool>

   :returns: bool

.. object:: objectTemplate.collisionGroups <U32>

   :returns: U32

.. object:: objectTemplate.collisionMesh <std::string>

   :returns: void

.. object:: objectTemplate.collisionMesh <std::string>

   :returns: std::string

.. object:: objectTemplate.collisionPart <int>

   :returns: int

.. object:: objectTemplate.collisionSpeedAlongNormal <float>

   :returns: float

.. object:: objectTemplate.collisionSpeedAlongPlane <float>

   :returns: float

.. object:: objectTemplate.collisionStartRadius <float>

   :returns: float

.. object:: objectTemplate.color <Vec3ColorFloatIntensity>

   :returns: Vec3ColorFloatIntensity

.. object:: objectTemplate.color <Vec3ColorFloat>

   :returns: Vec3ColorFloat

.. object:: objectTemplate.color1 <Vec3ColorFloatIntensity>

   :returns: Vec3ColorFloatIntensity

.. object:: objectTemplate.color2 <Vec3ColorFloatIntensity>

   :returns: Vec3ColorFloatIntensity

.. object:: objectTemplate.colorBlendGraph <Vec4>

   :returns: Vec4

.. object:: objectTemplate.coneAngle1 <float>

   :returns: float

.. object:: objectTemplate.coneAngle2 <float>

   :returns: float

.. object:: objectTemplate.coneDirection <Vec3>

   :returns: Vec3

.. object:: objectTemplate.coneInnerAngle <float>

   :returns: float

.. object:: objectTemplate.coneOuterAngle <float>

   :returns: float

.. object:: objectTemplate.coneOuterVolume <float>

   :returns: float

.. object:: objectTemplate.constantForce <float>

   :returns: float

.. object:: objectTemplate.constantRpm <bool>

   :returns: bool

.. object:: objectTemplate.continousRotationSpeed <Math::Vec3>

   :returns: Math::Vec3

.. object:: objectTemplate.controlPointId <int>

   :returns: int

.. object:: objectTemplate.ControlPointId <U32>

   :returns: U32

.. object:: objectTemplate.controlPointName <std::string>

   :returns: std::string

.. object:: objectTemplate.controlsCategory <dice::hfe::world::VehicleCategory>

   :returns: dice::hfe::world::VehicleCategory

.. object:: objectTemplate.coolDownPerSec <float>

   :returns: float

.. object:: objectTemplate.coolingFactor <float>

   :returns: float

.. object:: objectTemplate.copyLinksCount <int>

   :returns: int

.. object:: ObjectTemplate.create <std::string std::string>

   :returns: IObjectTemplate\*

.. object:: objectTemplate.createComponent <std::string>

   :returns: void

.. object:: objectTemplate.createdInEditor <bool>

   :returns: bool

.. object:: objectTemplate.createInvisible <bool>

   :returns: bool

   - Creates the object as invisible.
   - Collisions and Functions still work.
   - Tested on the ``at_mine``

.. object:: objectTemplate.createNotInGrid <bool>

   :returns: bool

.. object:: objectTemplate.createVisibleInEditor <bool>

   :returns: bool

.. object:: objectTemplate.crewKitIndex <int>

   :returns: int

   - :file:`kits.con` (example: :file:`gb82_pilot.con`)
   - Defines what Geom to use for the kit.
   - Looks up the Geom1 etc in the :file:`.skinnedmesh`, which is located in the Meshes folder. For example, arg82/Meshes/arg82_kits1.skinnedmeshes.
   - Open with BfMeshViewer to know what each number looks like.

.. object:: objectTemplate.crosshairFireTime <float>

   :returns: float

.. object:: objectTemplate.cullRadiusScale <float>

   :returns: float

   Used in Weapons, Vehicle, Statics etc.

.. object:: objectTemplate.CVMChase <bool>

   :returns: bool

   - Vehicle :file:`.tweak` files
   - Used to set at what distance the object is culled from display.
   - Each number represents a distance of 25m.
   - For example: ``ObjectTemplate.cullRadiusScale 6`` - VD of 150m

.. object:: objectTemplate.CVMExternTrace <bool>

   :returns: bool

   Vehicle :file:`.tweak` files

.. object:: objectTemplate.CVMFlyBy <bool>

   :returns: bool

   Vehicle :file:`.tweak` files

.. object:: objectTemplate.CVMFrontChase <bool>

   :returns: bool

   Vehicle :file:`.tweak` files

.. object:: objectTemplate.CVMInside <bool>

   :returns: bool

   Vehicle :file:`.tweak` files

.. object:: objectTemplate.CVMNose <bool>

   :returns: bool

   Vehicle :file:`.tweak` files

.. object:: objectTemplate.CVMTrace <bool>

   :returns: bool

   Vehicles :file:`.tweak` files

.. object:: objectTemplate.cycles <int>

   :returns: int

.. object:: objectTemplate.damage <float>

   :returns: float

.. object:: objectTemplate.damagedAmbientSoundLimit <float>

   :returns: float

.. object:: objectTemplate.damageForBeingOutSideWorld <float>

   :returns: float

.. object:: objectTemplate.damageMandownSoldiers <bool>

   :returns: bool

.. object:: objectTemplate.damageOwner <bool>

   :returns: bool

.. object:: objectTemplate.damageSpeed <float>

   :returns: float

.. object:: objectTemplate.damageWhenLost <float>

   :returns: float

.. object:: objectTemplate.dampenSprintRotationalForceInAirMod <float>

   :returns: float

.. object:: objectTemplate.dampHorizontalVel <float>

   :returns: float

.. object:: objectTemplate.dampHorizontalVelFactor <float>

   :returns: float

.. object:: objectTemplate.damping <float>

   :returns: float

.. object:: objectTemplate.deAcceleration <Math::Vec3>

   :returns: Math::Vec3

.. object:: objectTemplate.debugAutoRotate <bool>

   :returns: bool

.. object:: objectTemplate.debugForceGearUp <bool>

   :returns: bool

.. object:: objectTemplate.decalTextureName <std::string>

   :returns: std::string

.. object:: objectTemplate.decreaseAngleToZero <bool>

   :returns: bool

.. object:: objectTemplate.decreaseAngleToZeroSpeed <float>

   :returns: float

.. object:: objectTemplate.decreaseAngleToZeroVerticalVel <float>

   :returns: float

.. object:: objectTemplate.defaultAngleOfAttack <float>

   :returns: float

.. object:: objectTemplate.defaultWeaponIndex <int>

   :returns: int

.. object:: objectTemplate.degradeDropStrength <float>

   :returns: float

.. object:: objectTemplate.degradeThrowStrength <float>

   :returns: float

.. object:: objectTemplate.degradeThrowStrength2 <float>

   :returns: float

.. object:: objectTemplate.delay <RandomDistribution>

   :returns: RandomDistribution

.. object:: objectTemplate.delayBeforeCycle <float>

   :returns: float

.. object:: objectTemplate.delayBeforeEnd <float>

   :returns: float

.. object:: objectTemplate.delayBeforeStart <float>

   :returns: float

.. object:: objectTemplate.delayToUse <float>

   :returns: float

.. object:: ObjectTemplate.delete <world::IObjectTemplate_ptrproxy>

   :returns: void

.. object:: objectTemplate.deleteComponent <std::string>

   :returns: void

.. object:: objectTemplate.deployAnimationTime <float>

   :returns: float

.. object:: objectTemplate.destroyableWindowsTemplate <std::string>

   :returns: std::string

.. object:: objectTemplate.destroyOnExit <bool>

   :returns: bool

.. object:: objectTemplate.destroyWhenEmptyStorage <bool>

   :returns: bool

.. object:: objectTemplate.detonateAfterProjectileStopped <bool>

   :returns: bool

.. object:: objectTemplate.detonateAfterProjectileStoppedMinSpeed <float>

   :returns: float

.. object:: objectTemplate.detonation.allowFriendlyFireDetonation <bool>

   :returns: bool

.. object:: objectTemplate.detonation.detectionRadius <float>

   :returns: float

.. object:: objectTemplate.detonation.detonateDistanceToTarget <float>

   :returns: float

.. object:: objectTemplate.detonation.detonateOnWaterCollision <bool>

   :returns: bool

.. object:: objectTemplate.detonation.effectRotation <Vec3>

   :returns: Vec3

.. object:: objectTemplate.detonation.endEffectTemplate <std::string>

   :returns: std::string

.. object:: objectTemplate.detonation.explosionConeAngle <float>

   :returns: float

.. object:: objectTemplate.detonation.explosionDamage <float>

   :returns: float

.. object:: objectTemplate.detonation.explosionForce <float>

   :returns: float

.. object:: objectTemplate.detonation.explosionInnerConeRadius <float>

   :returns: float

.. object:: objectTemplate.detonation.explosionLineOfSightMinimumDamage <float>

   :returns: float

.. object:: objectTemplate.detonation.explosionMaterial <int>

   :returns: int

.. object:: objectTemplate.detonation.explosionRadius <float>

   :returns: float

.. object:: objectTemplate.detonation.explosionSoldierLineOfSight <float>

   :returns: float

.. object:: objectTemplate.detonation.explosionSoldierLineOfSightHealRate <float>

   :returns: float

.. object:: objectTemplate.detonation.explosionSoldierLineOfSightTimer <float>

   :returns: float

.. object:: objectTemplate.detonation.explosionYMod <float>

   :returns: float

.. object:: objectTemplate.detonation.flashbangAdditiveGlowMaxAlpha <float>

   :returns: float

.. object:: objectTemplate.detonation.flashbangAdditiveGlowMaxHealTime <float>

   :returns: float

.. object:: objectTemplate.detonation.flashbangAdditiveGlowMaxHoldTime <float>

   :returns: float

.. object:: objectTemplate.detonation.flashbangAdditiveGlowMaxRampTime <float>

   :returns: float

.. object:: objectTemplate.detonation.flashbangAdditiveGlowMinAlpha <float>

   :returns: float

.. object:: objectTemplate.detonation.flashbangAdditiveGlowMinHealTime <float>

   :returns: float

.. object:: objectTemplate.detonation.flashbangAdditiveGlowMinHoldTime <float>

   :returns: float

.. object:: objectTemplate.detonation.flashbangBillboardMaxAlpha <float>

   :returns: float

.. object:: objectTemplate.detonation.flashbangBillboardMaxHealTime <float>

   :returns: float

.. object:: objectTemplate.detonation.flashbangBillboardMaxHoldTime <float>

   :returns: float

.. object:: objectTemplate.detonation.flashbangBillboardMaxRampTime <float>

   :returns: float

.. object:: objectTemplate.detonation.flashbangBillboardMinAlpha <float>

   :returns: float

.. object:: objectTemplate.detonation.flashbangBillboardMinHealTime <float>

   :returns: float

.. object:: objectTemplate.detonation.flashbangBillboardMinHoldTime <float>

   :returns: float

.. object:: objectTemplate.detonation.flashbangMotionBlurMaxAlpha <float>

   :returns: float

.. object:: objectTemplate.detonation.flashbangMotionBlurMaxHealTime <float>

   :returns: float

.. object:: objectTemplate.detonation.flashbangMotionBlurMaxHoldTime <float>

   :returns: float

.. object:: objectTemplate.detonation.flashbangMotionBlurMaxRampTime <float>

   :returns: float

.. object:: objectTemplate.detonation.flashbangMotionBlurMinAlpha <float>

   :returns: float

.. object:: objectTemplate.detonation.flashbangMotionBlurMinHealTime <float>

   :returns: float

.. object:: objectTemplate.detonation.flashbangMotionBlurMinHoldTime <float>

   :returns: float

.. object:: objectTemplate.detonation.flashbangRadiusWithNightVision <float>

   :returns: float

.. object:: objectTemplate.detonation.invisibleAtEndEffect <bool>

   :returns: bool

.. object:: objectTemplate.detonation.maxDepthForExplosion <float>

   :returns: float

.. object:: objectTemplate.detonation.minDetonationSpeed <float>

   :returns: float

.. object:: objectTemplate.detonation.playMaterialEffectAtSurface <bool>

   :returns: bool

.. object:: objectTemplate.detonation.radiusDetonateWithAirVehicles <bool>

   :returns: bool

.. object:: objectTemplate.detonation.replenishingStrength <float>

   :returns: float

.. object:: objectTemplate.detonation.replenishingType <ReplenishingType>

   :returns: ReplenishingType

.. object:: objectTemplate.detonation.showMineIndicationIcon <bool>

   :returns: bool

.. object:: objectTemplate.detonation.stopAtEndEffect <bool>

   :returns: bool

.. object:: objectTemplate.detonation.timeUntilCanDetonate <float>

   :returns: float

.. object:: objectTemplate.detonation.triggerAngle <float>

   :returns: float

.. object:: objectTemplate.detonation.triggerRadius <float>

   :returns: float

.. object:: objectTemplate.detonation.triggerTime <float>

   :returns: float

.. object:: objectTemplate.detonation.triggerType <RadiusTriggerType>

   :returns: RadiusTriggerType

.. object:: objectTemplate.detonation.triggerVictimMinSpeed <float>

   :returns: float

.. object:: objectTemplate.detonation.useCollisionNormal <bool>

   :returns: bool

.. object:: objectTemplate.detonation.useMMOnEndEffect <bool>

   :returns: bool

.. object:: objectTemplate.deviation.devModCrouch <float>

   :returns: float

.. object:: objectTemplate.deviation.devModLie <float>

   :returns: float

.. object:: objectTemplate.deviation.devModStand <float>

   :returns: float

.. object:: objectTemplate.deviation.devModZoom <float>

   :returns: float

.. object:: objectTemplate.deviation.fireDevAdd <float>

   :returns: float

.. object:: objectTemplate.deviation.fireDevMax <float>

   :returns: float

.. object:: objectTemplate.deviation.fireDevSub <float>

   :returns: float

.. object:: objectTemplate.deviation.minDev <float>

   :returns: float

.. object:: objectTemplate.deviation.miscDevAddJump <float>

   :returns: float

.. object:: objectTemplate.deviation.miscDevMax <float>

   :returns: float

.. object:: objectTemplate.deviation.miscDevSub <float>

   :returns: float

.. object:: objectTemplate.deviation.radius <float>

   :returns: float

.. object:: objectTemplate.deviation.setFireDev <float float float>

   :returns: void

.. object:: objectTemplate.deviation.setMiscDev <float float float>

   :returns: void

.. object:: objectTemplate.deviation.setSpeedDev <float float float>

   :returns: void

.. object:: objectTemplate.deviation.setTurnDev <float float float>

   :returns: void

.. object:: objectTemplate.deviation.speedDevAddForward <float>

   :returns: float

.. object:: objectTemplate.deviation.speedDevAddStrafe <float>

   :returns: float

.. object:: objectTemplate.deviation.speedDevMax <float>

   :returns: float

.. object:: objectTemplate.deviation.speedDevSub <float>

   :returns: float

.. object:: objectTemplate.deviation.subProjectileDev <float>

   :returns: float

.. object:: objectTemplate.deviation.turnDevAddPitch <float>

   :returns: float

.. object:: objectTemplate.deviation.turnDevAddYaw <float>

   :returns: float

.. object:: objectTemplate.deviation.turnDevMax <float>

   :returns: float

.. object:: objectTemplate.deviation.turnDevSub <float>

   :returns: float

.. object:: objectTemplate.differential <float>

   :returns: float

.. object:: objectTemplate.direction <Vec3>

   :returns: Vec3

.. object:: objectTemplate.directionalScale <float>

   :returns: float

.. object:: objectTemplate.disableIfEnemyInsideRadius <bool>

   :returns: bool

.. object:: objectTemplate.disableInputWhileDucking <bool>

   :returns: bool

.. object:: objectTemplate.disableSpawnPointsOnEnter <bool>

   :returns: bool

.. object:: objectTemplate.disableWhenEmptyVehicle <bool>

   :returns: bool

.. object:: objectTemplate.disableWhenEmptyVehicleDelay <float>

   :returns: float

.. object:: objectTemplate.disableWhenLosingControl <bool>

   :returns: bool

.. object:: objectTemplate.disableWhenWreck <bool>

   :returns: bool

.. object:: objectTemplate.dismountAngle <float>

   :returns: float

.. object:: objectTemplate.dismountCheckOffset <float>

   :returns: float

.. object:: objectTemplate.distance <float>

   :returns: float

.. object:: objectTemplate.distanceCannotEnter <float>

   :returns: float

.. object:: objectTemplate.distToMinDamage <float>

   :returns: float

.. object:: objectTemplate.distToStartLoseDamage <float>

   :returns: float

.. object:: objectTemplate.dontAllowExit <bool>

   :returns: bool

.. object:: objectTemplate.dontClearTeamOnExit <bool>

   :returns: bool

.. object:: objectTemplate.drag <float>

   :returns: float

   - How much the drag from the body of a vehicle affects its speed.
   - Without it, a vehicle will have an infinite top speed.

.. object:: objectTemplate.drag <RandomDistribution>

   :returns: RandomDistribution

.. object:: objectTemplate.dragModifier <Vec3>

   :returns: Vec3

.. object:: objectTemplate.dragModifier <float>

   :returns: float

.. object:: objectTemplate.dragOffset <Vec3>

   :returns: Vec3

   To offset the drag using 0/0/0 - ``X/Y/Z``

.. object:: objectTemplate.dragOverTime <OverTimeDistribution>

   :returns: OverTimeDistribution

.. object:: objectTemplate.drawOrder <std::string>

   :returns: std::string

.. object:: objectTemplate.dropHeadwear <std::string>

   :returns: std::string

.. object:: objectTemplate.dropStrength <float>

   :returns: float

.. object:: objectTemplate.effectChangeWaterHeight <float>

   :returns: float

.. object:: objectTemplate.effectOnSpawn <std::string>

   :returns: std::string

.. object:: objectTemplate.effectTemplateBaseName <std::string>

   :returns: std::string

.. object:: objectTemplate.elasticity <float>

   :returns: float

.. object:: objectTemplate.emitDelay <float>

   :returns: float

.. object:: objectTemplate.emitDirection <Vec3>

   :returns: Vec3

.. object:: objectTemplate.emitDirectionZFromSpeedDof <bool>

   :returns: bool

.. object:: objectTemplate.emitFrequency <float>

   :returns: float

.. object:: objectTemplate.emitFrequencyScaleFactorLowerBound <float>

   :returns: float

.. object:: objectTemplate.emitPrio <std::string>

   :returns: std::string

.. object:: objectTemplate.emitRadius <Vec3>

   :returns: Vec3

.. object:: objectTemplate.emitRangeX <RandomDistribution>

   :returns: RandomDistribution

.. object:: objectTemplate.emitRangeY <RandomDistribution>

   :returns: RandomDistribution

.. object:: objectTemplate.emitRangeZ <RandomDistribution>

   :returns: RandomDistribution

.. object:: objectTemplate.emitScaleFactorFromAcceleration <Vec2>

   :returns: Vec2

.. object:: objectTemplate.emitScaleFactorFromAltitude <Vec2>

   :returns: Vec2

.. object:: objectTemplate.emitScaleFactorFromEngine <Vec2>

   :returns: Vec2

.. object:: objectTemplate.emitScaleFactorFromRotationalSpeed <Vec2>

   :returns: Vec2

.. object:: objectTemplate.emitScaleFactorFromSpeed <Vec2>

   :returns: Vec2

.. object:: objectTemplate.emitScaleFactorFromSpeedInDof <Vec2>

   :returns: Vec2

.. object:: objectTemplate.emitScaleFactorRange <Vec2>

   :returns: Vec2

.. object:: objectTemplate.emitScaleFactorUsed <bool>

   :returns: bool

.. object:: objectTemplate.emitSpeed <float>

   :returns: float

.. object:: objectTemplate.emitSpeedGraph <Vec4>

   :returns: Vec4

.. object:: objectTemplate.emitSpeedScaleFromAcceleration <Vec2>

   :returns: Vec2

.. object:: objectTemplate.emitSpeedScaleFromAltitude <Vec2>

   :returns: Vec2

.. object:: objectTemplate.emitSpeedScaleFromEngine <Vec2>

   :returns: Vec2

.. object:: objectTemplate.emitSpeedScaleFromRotationalSpeed <Vec2>

   :returns: Vec2

.. object:: objectTemplate.emitSpeedScaleFromSpeed <Vec2>

   :returns: Vec2

.. object:: objectTemplate.emitSpeedScaleFromSpeedInDof <Vec2>

   :returns: Vec2

.. object:: objectTemplate.emitSpeedScaleRange <Vec2>

   :returns: Vec2

.. object:: objectTemplate.emitSpeedScaleUsed <bool>

   :returns: bool

.. object:: objectTemplate.emitterSpeedScale <float>

   :returns: float

.. object:: objectTemplate.emitterType <std::string>

   :returns: std::string

.. object:: objectTemplate.emitTime <float>

   :returns: float

.. object:: objectTemplate.enabled <bool>

   :returns: bool

.. object:: objectTemplate.enemyTicketLossWhenCaptured <int>

   :returns: int

.. object:: objectTemplate.engineInfluence <float>

   :returns: float

.. object:: objectTemplate.engineName <std::string>

   :returns: std::string

.. object:: objectTemplate.engineType <int>

   :returns: int

   - What kind of vehicle the engine is for.
   - Car, tank, plane, ship, or helicopter.

.. object:: objectTemplate.entryRadius <float>

   :returns: float

.. object:: objectTemplate.events <int>

   :returns: int

.. object:: objectTemplate.exitSpeedMod <float>

   :returns: float

.. object:: objectTemplate.fadeInFactor <float>

   :returns: float

.. object:: objectTemplate.fadeOutFactor <float>

   :returns: float

.. object:: objectTemplate.fire.addBarrelName <std::string>

   :returns: void

.. object:: objectTemplate.fire.addFireRate <int>

   :returns: void

   - Used in Weapons and Vehicle :file:`.tweak`
   - Defines the fire mode selector. You can add three lines max of each one.

      :0: Single
      :1: Burst
      :2: Auto

.. object:: objectTemplate.fire.addTimeEvent <WeaponTrigger WeaponAction float>

   :returns: void

.. object:: objectTemplate.fire.altFireInput <io::PlayerInputMap>

   :returns: io::PlayerInputMap

   Which PlayerInput map to use for the right-click function. Usually ``PIAlt``

.. object:: objectTemplate.fire.batchSize <int>

   :returns: int

.. object:: objectTemplate.fire.burstSize <int>

   :returns: int

.. object:: objectTemplate.fire.busyUntilButtonRelease <bool>

   :returns: bool

.. object:: objectTemplate.fire.detonatorObject <std::string>

   :returns: std::string

.. object:: objectTemplate.fire.dropLod <int>

   :returns: int

.. object:: objectTemplate.fire.dropWeaponAfterFiringDelay <float>

   :returns: float

.. object:: objectTemplate.fire.dropWeaponAfterReloadDelay <float>

   :returns: float

.. object:: objectTemplate.fire.fireInCameraDof <bool>

   :returns: bool

.. object:: objectTemplate.fire.fireInCameraDofLocked <bool>

   :returns: bool

.. object:: objectTemplate.fire.fireInput <io::PlayerInputMap>

   :returns: io::PlayerInputMap

.. object:: objectTemplate.fire.fireLaunchDelay <float>

   :returns: float

.. object:: objectTemplate.fire.fireLaunchDelaySoft <float>

   :returns: float

.. object:: objectTemplate.fire.fireStartDelay <RandomDistribution>

   :returns: RandomDistribution

.. object:: objectTemplate.fire.hideLod <int>

   :returns: int

.. object:: objectTemplate.fire.hideWeaponAfterFiringDelay <float>

   :returns: float

.. object:: objectTemplate.fire.hideWeaponAfterReloadDelay <float>

   :returns: float

.. object:: objectTemplate.fire.ignoreFireButton <io::PlayerInputMap>

   :returns: io::PlayerInputMap

.. object:: objectTemplate.fire.isBarrel <std::string>

   :returns: bool

.. object:: objectTemplate.fire.maxProjectilesInWorld <int>

   :returns: int

   - The max amount of projectiles in the weapon that can be set before the engine cleans up each one.
   - If the limit is 10, deploying one any further will delete an existing projectile.
   - Used for explosives, mines, and maybe bullets.

.. object:: objectTemplate.fire.onlyFireWhenProne <bool>

   :returns: bool

   Restricts the weapon to fire only when prone.

   Though when firing during prone, a player can then stand and run to deploy an explosive for example. FH2 uses these for the machine gunner kits

.. object:: objectTemplate.fire.projectileStartPosition <Vec3>

   :returns: Vec3

   Position in X/Y/Z from the crosshair or PCO from where the projectile will launch.

.. object:: objectTemplate.fire.projectileStartRotation <Vec3>

   :returns: Vec3

.. object:: objectTemplate.fire.pullbackTime <float>

   :returns: float

.. object:: objectTemplate.fire.radioMessageDelay <float>

   :returns: float

.. object:: objectTemplate.fire.randomRotationSpeed <float>

   :returns: float

.. object:: objectTemplate.fire.removeBarrelName <std::string>

   :returns: void

.. object:: objectTemplate.fire.roundsPerMinute <int>

   :returns: int

   - Used in GenericFirearms (Weapons, Projectiles)
   - The rate of fire, measured in Rounds Per Minute (RPM).
   - Must be dividable by 1800.
   - Check: http://researchmaniacs.com/Math/Divisible-By/What-is-1800-divisible-by.html

.. object:: objectTemplate.fire.showWeaponAfterReloadDelay <float>

   :returns: float

.. object:: objectTemplate.fire.timeToReachMaxStrengthSlow <float>

   :returns: float

.. object:: objectTemplate.fire.toggleWeaponTime <float>

   :returns: float

.. object:: objectTemplate.fire.triggerChargesTime <float>

   :returns: float

.. object:: objectTemplate.fire.useDummyProjectiles <bool>

   :returns: bool

.. object:: objectTemplate.fixAxisSpring <bool>

   :returns: bool

.. object:: objectTemplate.flagTemplateTeam0 <std::string>

   :returns: std::string

.. object:: objectTemplate.flagTemplateTeam1 <std::string>

   :returns: std::string

.. object:: objectTemplate.flagTemplateTeam2 <std::string>

   :returns: std::string

.. object:: objectTemplate.flapLift <float>

   :returns: float

.. object:: objectTemplate.flicker <float>

   :returns: float

.. object:: objectTemplate.floaterMod <float>

   :returns: float

.. object:: objectTemplate.floatMaxLift <float>

   :returns: float

.. object:: objectTemplate.floatMinLift <float>

   :returns: float

.. object:: objectTemplate.follow.changePitch <float>

   :returns: float

.. object:: objectTemplate.follow.changeYaw <float>

   :returns: float

.. object:: objectTemplate.follow.maxPitch <float>

   :returns: float

.. object:: objectTemplate.follow.maxYaw <float>

   :returns: float

.. object:: objectTemplate.follow.minDist <float>

   :returns: float

.. object:: objectTemplate.followStiffness <float>

   :returns: float

.. object:: objectTemplate.force <float>

   :returns: float

.. object:: objectTemplate.forceSustainedFire <bool>

   :returns: bool

.. object:: objectTemplate.forceToWaterSurface <bool>

   :returns: bool

.. object:: objectTemplate.ForSoldierOnly <bool>

   :returns: bool

.. object:: objectTemplate.fov <float>

   :returns: float

.. object:: objectTemplate.gasCloudDamage <float>

   :returns: float

.. object:: objectTemplate.gasCloudRadiusTime <float>

   :returns: float

.. object:: objectTemplate.gasCloudType <geom::GasCloudType>

   :returns: geom::GasCloudType

.. object:: objectTemplate.gasMaskSprintFactor <float>

   :returns: float

.. object:: objectTemplate.gearChangeTime <float>

   :returns: float

.. object:: objectTemplate.gearDown <float>

   :returns: float

.. object:: objectTemplate.gearDownDelay <float>

   :returns: float

.. object:: objectTemplate.gearDownHeight <float>

   :returns: float

.. object:: objectTemplate.gearDownSpeed <float>

   :returns: float

.. object:: objectTemplate.gearUp <float>

   :returns: float

.. object:: objectTemplate.gearUpDelay <float>

   :returns: float

.. object:: objectTemplate.gearUpHeight <float>

   :returns: float

.. object:: objectTemplate.gearUpSpeed <float>

   :returns: float

.. object:: objectTemplate.geometry <std::string>

   :returns: std::string

.. object:: objectTemplate.geometry.dropGeom <int>

   :returns: int

.. object:: objectTemplate.geometry.kit <int>

   :returns: int

.. object:: objectTemplate.geometry1P <std::string>

   :returns: void

.. object:: objectTemplate.geometry3P <std::string>

   :returns: void

.. object:: objectTemplate.geometryPart <int>

   :returns: int

.. object:: objectTemplate.getHeatBarType

   :returns: int

.. object:: objectTemplate.getPosition <int>

   :returns: Math::Vec3

.. object:: objectTemplate.getRotation <int>

   :returns: Math::Vec3

.. object:: objectTemplate.getTemplate <int>

   :returns: std::string

.. object:: objectTemplate.globalEffectLevel <float>

   :returns: float

.. object:: objectTemplate.gravity <float>

   :returns: float

   Sets the gravity for the map. Can use minus values as well

.. object:: objectTemplate.gravityGraph <Vec4>

   :returns: Vec4

.. object:: objectTemplate.gravityModifier <float>

   :returns: float

   - Sets the gravity for the vehicle.
   - Can use minus values as well which makes the projectile go upwards

.. object:: objectTemplate.gravityModifier <RandomDistribution>

   :returns: RandomDistribution

.. object:: objectTemplate.gravityModifierOverTime <OverTimeDistribution>

   :returns: OverTimeDistribution

.. object:: objectTemplate.grip <PhysicsGripFlags>

   :returns: PhysicsGripFlags

   - Set only for wheels.
   - Roll grip for wheels that are not powered.
   - Engine grip for wheels that are powered.
   - Engine dummy grip for wheel you want to make looking like they are powered, but actually aren't.

.. object:: objectTemplate.groundContactVolume <float>

   :returns: float

.. object:: objectTemplate.group <U32>

   :returns: U32

.. object:: objectTemplate.halfVolumeDistance <float>

   :returns: float

.. object:: objectTemplate.handleCollisionSpeed <float>

   :returns: float

.. object:: objectTemplate.hasAltEffect <bool>

   :returns: bool

.. object:: objectTemplate.hasCollisionPhysics <bool>

   :returns: bool

   - Check for all objects that has a collision mesh.
   - Allows it to be hit by both bullets, players, and vehicles

.. object:: objectTemplate.HasGreyCapturingState <bool>

   :returns: bool

.. object:: objectTemplate.hasMobilePhysics <bool>

   :returns: bool

   Check for objects and parts that can move.

.. object:: objectTemplate.hasOnTimeEffect <bool>

   :returns: bool

.. object:: objectTemplate.hasOverDamage <bool>

   :returns: bool

.. object:: objectTemplate.hasPartner <bool>

   :returns: bool

.. object:: objectTemplate.hasPointPhysics <bool>

   :returns: void

.. object:: objectTemplate.hasRelativeOffset <bool>

   :returns: bool

.. object:: objectTemplate.hasResponsePhysics <bool>

   :returns: void

.. object:: objectTemplate.hasRestrictedExit <bool>

   :returns: bool

.. object:: objectTemplate.hasRotationalPointPhysics <bool>

   :returns: void

.. object:: objectTemplate.HDRIntensity <float>

   :returns: float

.. object:: objectTemplate.healSpeed <float>

   :returns: float

.. object:: objectTemplate.healStorageSize <float>

   :returns: float

.. object:: objectTemplate.heatAddWhenFire <float>

   :returns: float

.. object:: objectTemplate.heatIncrement <float>

   :returns: float

.. object:: objectTemplate.height <float>

   :returns: float

.. object:: objectTemplate.heightOffset <float>

   :returns: float

.. object:: objectTemplate.helpHud.altHelpSoundKey <std::string>

   :returns: std::string

.. object:: objectTemplate.helpHud.altHelpstd::stringKey <std::string>

   :returns: std::string

.. object:: objectTemplate.helpHud.closeToDistance <int>

   :returns: int

.. object:: objectTemplate.helpHud.closeToHelpSoundKeyEnemy <std::string>

   :returns: std::string

.. object:: objectTemplate.helpHud.closeToHelpSoundKeyFriendly <std::string>

   :returns: std::string

.. object:: objectTemplate.helpHud.closeToHelpSoundKeyNeutral <std::string>

   :returns: std::string

.. object:: objectTemplate.helpHud.closeToHelpstd::stringKeyEnemy <std::string>

   :returns: std::string

.. object:: objectTemplate.helpHud.closeToHelpstd::stringKeyFriendly <std::string>

   :returns: std::string

.. object:: objectTemplate.helpHud.closeToHelpstd::stringKeyNeutral <std::string>

   :returns: std::string

.. object:: objectTemplate.helpHud.helpSoundKey <std::string>

   :returns: std::string

.. object:: objectTemplate.helpHud.helpstd::stringKey <std::string>

   :returns: std::string

.. object:: objectTemplate.helpHud.lowAmmoHelpSoundKey <std::string>

   :returns: std::string

.. object:: objectTemplate.helpHud.lowAmmoHelpstd::stringKey <std::string>

   :returns: std::string

.. object:: objectTemplate.helpHud.lowArmorHelpSoundKey <std::string>

   :returns: std::string

.. object:: objectTemplate.helpHud.lowArmorHelpstd::stringKey <std::string>

   :returns: std::string

.. object:: objectTemplate.hideFirstPerson <bool>

   :returns: bool

.. object:: objectTemplate.hoistFlag <bool>

   :returns: bool

.. object:: objectTemplate.hoistMinMax <Vec2>

   :returns: Vec2

.. object:: objectTemplate.holdObject <bool>

   :returns: bool

.. object:: objectTemplate.horizontalDampAngle <float>

   :returns: float

.. object:: objectTemplate.horizontalDampAngleFactor <float>

   :returns: float

.. object:: objectTemplate.horizontalSpeedMagnifier <float>

   :returns: float

.. object:: objectTemplate.hullHeight <float>

   :returns: float

.. object:: objectTemplate.ik.poleVectorLeft <Vec3>

   :returns: Vec3

.. object:: objectTemplate.ik.poleVectorRight <Vec3>

   :returns: Vec3

.. object:: objectTemplate.ik.positionLeft <Vec3>

   :returns: Vec3

.. object:: objectTemplate.ik.positionRight <Vec3>

   :returns: Vec3

.. object:: objectTemplate.ik.rotationLeft <Vec3>

   :returns: Vec3

.. object:: objectTemplate.ik.rotationRight <Vec3>

   :returns: Vec3

.. object:: objectTemplate.inertiaModifier <Vec3>

   :returns: Vec3

.. object:: ObjectTemplate.info <world::IObjectTemplate_ptrproxy>

   :returns: std::string

.. object:: objectTemplate.inheritHeatFromPrimary <bool>

   :returns: bool

.. object:: objectTemplate.initiallyWalkable <bool>

   :returns: bool

.. object:: objectTemplate.input <io::PlayerInputMap>

   :returns: io::PlayerInputMap

.. object:: objectTemplate.inputToPitch <io::PlayerInputMap>

   :returns: io::PlayerInputMap

.. object:: objectTemplate.inputToRoll <io::PlayerInputMap>

   :returns: io::PlayerInputMap

.. object:: objectTemplate.inputToYaw <io::PlayerInputMap>

   :returns: io::PlayerInputMap

.. object:: objectTemplate.insideDamageFrequency <float>

   :returns: float

.. object:: objectTemplate.insideDamageThreshold <float>

   :returns: float

.. object:: objectTemplate.insideFOV <float>

   :returns: float

.. object:: objectTemplate.insideStaticSunAmbientColor <Vec3ColorFloatIntensity>

   :returns: Vec3ColorFloatIntensity

.. object:: objectTemplate.insideStaticSunColor <Vec3ColorFloatIntensity>

   :returns: Vec3ColorFloatIntensity

.. object:: objectTemplate.insideStaticSunDamageColor <Vec3ColorFloatIntensity>

   :returns: Vec3ColorFloatIntensity

.. object:: objectTemplate.insideStaticSunDirection <Vec3>

   :returns: Vec3

.. object:: objectTemplate.intensity <float>

   :returns: float

.. object:: objectTemplate.intensity <RandomDistribution>

   :returns: RandomDistribution

.. object:: objectTemplate.intensityAtSpeed <float>

   :returns: float

.. object:: objectTemplate.intensityOverTime <OverTimeDistribution>

   :returns: OverTimeDistribution

.. object:: objectTemplate.inventorySize <U32>

   :returns: U32

.. object:: objectTemplate.inverseHeatBar <bool>

   :returns: bool

.. object:: objectTemplate.invertGear <bool>

   :returns: bool

.. object:: objectTemplate.invisible <bool>

   :returns: bool

.. object:: objectTemplate.is3dSound <bool>

   :returns: bool

   If the :file:`.wav` file is Mono, setting it to 1 will tell the engine to play it on both channels. If applied to a :file:`.wav` that is Stereo, it will play on the entire map. Same with :file:`.wav` files though it's usually experimentation.

.. object:: objectTemplate.isCounterForce <bool>

   :returns: bool

.. object:: objectTemplate.isDestructable <bool>

   :returns: bool

   Check only if object is a destroyable static object.

.. object:: objectTemplate.isDynamic <bool>

   :returns: bool

.. object:: objectTemplate.isGasMask <bool>

   :returns: bool

.. object:: objectTemplate.isHemisphere <bool>

   :returns: bool

.. object:: objectTemplate.isLocalSystem <bool>

   :returns: bool

   - Makes the effect follow the projectile and allows it to arch.
   - Used for the M67 *Zippo* Tank Flamethrower Effect.
   - Without it, the flame effect just shoots straight but not following the projectile

.. object:: objectTemplate.isLooping <bool>

   :returns: bool

.. object:: objectTemplate.isNightVision <bool>

   :returns: bool

.. object:: objectTemplate.isNotSaveable <bool>

   :returns: bool

.. object:: objectTemplate.isOpenVehicle <bool>

   :returns: bool

   Allows the ragdoll to slide off when killed from a vehicle position. Used in Technicals. If this is option. the passenger animation must have a die animation specified otherwise the ragdolls will float in the air.

.. object:: objectTemplate.isOvergrowth <bool>

   :returns: bool

.. object:: objectTemplate.isPortalPassing <bool>

   :returns: bool

.. object:: objectTemplate.isSelectable <bool>

   :returns: bool

.. object:: objectTemplate.isSleeping <bool>

   :returns: bool

.. object:: objectTemplate.isStatic <bool>

   :returns: bool

.. object:: objectTemplate.isStaticSystem <bool>

   :returns: bool

.. object:: objectTemplate.isUnderwaterEffect <bool>

   :returns: bool

.. object:: objectTemplate.isUnstrategicControlPoint <bool>

   :returns: bool

.. object:: objectTemplate.itemIndex <int>

   :returns: int

   - What number in the keyboard is mapped to what weapon/tool.
   - Max is 9, not sure about 0.
   - Also positions the weapon icon square.

.. object:: objectTemplate.itemType <int>

   :returns: int

.. object:: objectTemplate.keepProjectiles <float>

   :returns: float Weapons

   - Time to keep the projectile in the world in seconds after you or the weapon dies

.. object:: objectTemplate.killHeatSeekingMissile <bool>

   :returns: bool

.. object:: objectTemplate.kitTeam <int>

   :returns: int

.. object:: objectTemplate.kitType <hfe::KitType>

   :returns: hfe::KitType

.. object:: objectTemplate.lesserYawAtSpeed <float>

   :returns: float

.. object:: objectTemplate.liftRegulated <bool>

   :returns: bool

.. object:: objectTemplate.LightAffectionFactor <float>

   :returns: float

.. object:: objectTemplate.lightMapIntensityOffset <float>

   :returns: float

.. object:: objectTemplate.lightType <std::string>

   :returns: std::string

.. object:: objectTemplate.linkAttachMovement <float>

   :returns: float

.. object:: objectTemplate.linkAttachTime <float>

   :returns: float

.. object:: objectTemplate.linkedEffectContainer <std::string>

   :returns: std::string

.. object:: ObjectTemplate.list <std::string>

   :returns: std::string

.. object:: objectTemplate.listenerObstruction <float>

   :returns: float

   - Vehicles :file:`.tweak`
   - How muffled is the sound.
   - Lower value is least muffled.

.. object:: ObjectTemplate.listTemplateClasses

   :returns: std::string

.. object:: objectTemplate.listTemplates

   :returns: std::string

.. object:: ObjectTemplate.loadAll

   :returns: bool

.. object:: objectTemplate.localPredictOnClient <bool>

   :returns: bool

   - Used with Grenades and if there's any effect projectiles.
   - Seems like it tells the server to predict what's going to happen.
   - Maybe used with the Networkable Setting

.. object:: objectTemplate.lodDistance <float>

   :returns: float

.. object:: objectTemplate.LodDistance <std::string>

   :returns: std::string

.. object:: objectTemplate.loopCount <int>

   :returns: int

.. object:: objectTemplate.looping <bool>

   :returns: bool

.. object:: objectTemplate.loseControlWhenEnemyClose <bool>

   :returns: bool

.. object:: objectTemplate.loseControlWhenNotClose <bool>

   :returns: bool

.. object:: objectTemplate.lowSamples <int>

   :returns: int

.. object:: objectTemplate.maintainCameraOnEnter <bool>

   :returns: bool

.. object:: objectTemplate.maintainCameraOnExit <bool>

   :returns: bool

.. object:: objectTemplate.manDownCameraOffsetInDof <float>

   :returns: float

.. object:: objectTemplate.manDownCameraOffsetInUp <float>

   :returns: float

.. object:: objectTemplate.mapMaterial <uint std::string uint>

   :returns: void

.. object:: objectTemplate.maskOffset <Vec3>

   :returns: Vec3

.. object:: objectTemplate.maskType <hfe::MaskObjectType>

   :returns: hfe::MaskObjectType

.. object:: objectTemplate.mass <float>

   :returns: float

   - Used in Vehicles, Deployables, etc.
   - Mass is the weight of the vehicle in KG and also taking into account the GravityModifier value

.. object:: objectTemplate.material <int>

   :returns: int

.. object:: objectTemplate.maxAngleOfAttack <float>

   :returns: float

.. object:: objectTemplate.maxCorner <Vec3>

   :returns: Vec3

.. object:: objectTemplate.maxDistance <float>

   :returns: float

.. object:: objectTemplate.maxDistanceUnderWaterSurface <float>

   :returns: float

.. object:: objectTemplate.maxGasCloudRadius <float>

   :returns: float

.. object:: objectTemplate.maxNrOfObjectSpawned <U32>

   :returns: U32

.. object:: objectTemplate.maxResetSpeed <Math::Vec3>

   :returns: Math::Vec3

.. object:: objectTemplate.MaxRopeLength <float>

   :returns: float

   Fastropes confirmed ?!?!?!?!

.. object:: objectTemplate.maxRotation <Math::Vec3>

   :returns: Math::Vec3

.. object:: objectTemplate.maxSpawnDelay <float>

   :returns: float

.. object:: objectTemplate.maxSpeed <Math::Vec3>

   :returns: Math::Vec3

.. object:: objectTemplate.maxSpeed <float>

   :returns: float

.. object:: objectTemplate.maxTracerScaler <float>

   :returns: float

   - Used in Projectiles (Weapons)
   - How long the tracer effect can be depending on projectile speed.
   - Reference: http://www.battlefieldsingleplayer.com/forum/index.php?showtopic-8592&mode-threaded&pid-84936

.. object:: objectTemplate.maxTriggerDistance <float>

   :returns: float

.. object:: objectTemplate.maxVertRegAngle <float>

   :returns: float

.. object:: objectTemplate.MaxZiplineLength <float>

   :returns: float

.. object:: objectTemplate.mediumSamples <int>

   :returns: int

.. object:: objectTemplate.minCorner <Vec3>

   :returns: Vec3

.. object:: objectTemplate.minDamage <float>

   :returns: float

.. object:: objectTemplate.minDistance <float>

   :returns: float

.. object:: objectTemplate.minDistanceUnderWaterSurface <float>

   :returns: float

.. object:: objectTemplate.minGasCloudRadius <float>

   :returns: float

.. object:: objectTemplate.minimapNameOffset <Vec2>

   :returns: Vec2

.. object:: objectTemplate.minimumTimeBetweenTriggering <float>

   :returns: float

   - :file:`AmbientObjects.con` (Map)
   - The time when the trigger will repeat again after entering the trigger radius.
   - Happens after the effect plays. In seconds.
   - Depends also on ``ObjectTemplate.chance``

.. object:: objectTemplate.minNrToTakeControl <U32>

   :returns: U32

.. object:: objectTemplate.minRotation <Math::Vec3>

   :returns: Math::Vec3

.. object:: objectTemplate.minSpawnDelay <float>

   :returns: float

.. object:: objectTemplate.minTimeBetweenActivation <float>

   :returns: float

.. object:: objectTemplate.minTracerScaler <float>

   :returns: float

.. object:: objectTemplate.minTrailVelocity <float>

   :returns: float

.. object:: objectTemplate.minYNormal <float>

   :returns: float

.. object:: objectTemplate.movementSpeed <float>

   :returns: float

.. object:: objectTemplate.movementType <int>

   :returns: int

.. object:: objectTemplate.moveToWaterSurface <bool>

   :returns: bool

.. object:: objectTemplate.name

   :returns: std::string

.. object:: objectTemplate.nameTagOffset <Vec3>

   :returns: Vec3

.. object:: objectTemplate.nearCullingEnable <bool>

   :returns: bool

.. object:: objectTemplate.networkableInfo <std::string>

   :returns: std::string

   - :file:`Networkables.con`
   - Needs to be set for objects that won't work online without them.
   - Depends on the way it's set and if it crashes immediately, is laggy, or crashes unexpectantly

.. object:: objectTemplate.neverDrawAs1p <bool>

   :returns: bool

   - Vehicle, Weapons, Effects
   - Makes the effect not draw in front of you when in 1p mode.
   - Link: http://www.realitymod.com/forum/f388-pr-bf2-community-modding/113277-1p-animations-pcos-3.html

.. object:: objectTemplate.newCar2.brakeTorque <float>

   :returns: float

.. object:: objectTemplate.newCar2.engineBrakeTorque <float>

   :returns: float

.. object:: objectTemplate.newCar2.engineFeedbackMod <float>

   :returns: float

.. object:: objectTemplate.newCar2.frictionMod <float>

   :returns: float

.. object:: objectTemplate.newCar2.frictionTorque <float>

   :returns: float

.. object:: objectTemplate.newCar2.maxRpm <float>

   :returns: float

.. object:: objectTemplate.newCar2.minRpm <float>

   :returns: float

.. object:: objectTemplate.newCar2.slopeTorqueMod <float>

   :returns: float

.. object:: objectTemplate.newCar2.useClutchedTorque <bool>

   :returns: bool

.. object:: objectTemplate.newCar2.wheelInertia <float>

   :returns: float

.. object:: objectTemplate.newCar2.wheelLatDriveFrictionMod <float>

   :returns: float

.. object:: objectTemplate.newCar2.wheelLatFrictionMod <float>

   :returns: float

.. object:: objectTemplate.newCar2.wheelLatMinDynamicFriction <float>

   :returns: float

.. object:: objectTemplate.newCar2.wheelLatPeakAt <float>

   :returns: float

.. object:: objectTemplate.newCar2.wheelLatScale <float>

   :returns: float

.. object:: objectTemplate.newCar2.wheelLongDriveFrictionMod <float>

   :returns: float

.. object:: objectTemplate.newCar2.wheelLongFrictionMod <float>

   :returns: float

.. object:: objectTemplate.newCar2.wheelLongMinDynamicFriction <float>

   :returns: float

.. object:: objectTemplate.newCar2.wheelLongPeakAt <float>

   :returns: float

.. object:: objectTemplate.newCar2.wheelLongScale <float>

   :returns: float

.. object:: objectTemplate.noEffectAtPerpSpeed <float>

   :returns: float

.. object:: objectTemplate.noPassengerTimeToLive <int>

   :returns: int

.. object:: objectTemplate.noPhysics <bool>

   :returns: bool

.. object:: objectTemplate.noPropellerEffectAtSpeed <float>

   :returns: float

.. object:: objectTemplate.nosePos <Vec3>

   :returns: Vec3

.. object:: objectTemplate.notCycledIfOccupied <bool>

   :returns: bool

.. object:: objectTemplate.noVertRegAngle <float>

   :returns: float

.. object:: objectTemplate.nrOfObjectToSpawn <int>

   :returns: int

.. object:: objectTemplate.nrOfRespawns <int>

   :returns: int

.. object:: objectTemplate.numberOfGears <int>

   :returns: int

.. object:: objectTemplate.NumberOfLinks <int>

   :returns: int

.. object:: objectTemplate.numNetworkedEffects <int>

   :returns: int

.. object:: objectTemplate.numPlanes <int>

   :returns: int

.. object:: objectTemplate.objectShadows <bool>

   :returns: bool

.. object:: objectTemplate.objectTemplate <std::string>

   :returns: std::string

.. object:: objectTemplate.onlyTakeableByTeam <U32>

   :returns: U32

.. object:: objectTemplate.onlyWhenOccupied <bool>

   :returns: bool

.. object:: objectTemplate.otherCollisionLod <int>

   :returns: int

.. object:: objectTemplate.overheatPenalty <float>

   :returns: float

.. object:: objectTemplate.pan <float>

   :returns: float

.. object:: objectTemplate.ParticleMaxSize <float>

   :returns: float

   - Used in Vehicle :file:`.con` and :file:`.con` files
   - Defines what materials the vehicle should use, which references the materialdefine file.
   - Use BfMeshViewer to find out what numbers belong to what sides.

.. object:: objectTemplate.particleSystemTemplate <std::string>

   :returns: std::string

   Same as above

.. object:: objectTemplate.particleType <std::string>

   :returns: std::string

.. object:: objectTemplate.pcoFlags <int>

   :returns: int

.. object:: objectTemplate.pcoId <int>

   :returns: int

.. object:: objectTemplate.penetrate.allowLiquidPenetration <bool>

   :returns: bool

.. object:: objectTemplate.penetrate.allowSolidPenetration <bool>

   :returns: bool

.. object:: objectTemplate.penetrate.neverPenetrate <bool>

   :returns: bool

.. object:: objectTemplate.physicsFrequency <int>

   :returns: int

.. object:: objectTemplate.physicsType <PhysicsType>

   :returns: PhysicsType

   - Vehicles
   - ``None`` for no collision
   - ``Point`` for projectile (Ignores mesh)
   - ``Mesh`` if object has collision mesh

.. object:: objectTemplate.pitch <float>

   :returns: float

.. object:: objectTemplate.pitchEnvelope <std::string>

   :returns: std::string

.. object:: objectTemplate.pitchOffset <float>

   :returns: float

.. object:: objectTemplate.pivotOffset <Vec2>

   :returns: Vec2

.. object:: objectTemplate.PivotPosition <Math::Vec3>

   :returns: Math::Vec3

.. object:: objectTemplate.playAtEventPosition <bool>

   :returns: bool

.. object:: objectTemplate.playAtPlayerPosition <bool>

   :returns: bool

.. object:: objectTemplate.portalPassingPosition <Vec3>

   :returns: Vec3

.. object:: objectTemplate.poseCameraPosition <int Vec3>

   :returns: void

.. object:: objectTemplate.position <Vec3>

   :returns: Vec3

.. object:: objectTemplate.positionalSpeedInDof <RandomDistribution>

   :returns: RandomDistribution

.. object:: objectTemplate.positionalSpeedInRight <RandomDistribution>

   :returns: RandomDistribution

.. object:: objectTemplate.positionalSpeedInUp <RandomDistribution>

   :returns: RandomDistribution

.. object:: objectTemplate.positionOffset <Math::Vec3>

   :returns: Math::Vec3

.. object:: objectTemplate.postProcess.tvDistortionFreq <float>

   :returns: float

.. object:: objectTemplate.postProcess.tvDistortionRoll <float>

   :returns: float

.. object:: objectTemplate.postProcess.tvDistortionScale <float>

   :returns: float

.. object:: objectTemplate.postProcess.tvInterference <float>

   :returns: float

.. object:: objectTemplate.preCacheObject <bool>

   :returns: bool

.. object:: objectTemplate.preWarmTime <float>

   :returns: float

.. object:: ObjectTemplate.printScript <world::IObjectTemplate_ptrproxy>

   :returns: std::string

.. object:: objectTemplate.projectileTemplate <std::string>

   :returns: std::string

   - Used in Weapons and Vehicle :file:`.tweak`
   - GenericFirearm
   - Defines the projectile that the ``GenericFirearm`` should use.
   - Looks for the ``GenericProjectile`` that is defined in all :file:`.tweak` files.

.. object:: objectTemplate.projectOnHeightmap <bool>

   :returns: bool

.. object:: objectTemplate.projectorApplyMask <bool>

   :returns: bool

.. object:: objectTemplate.projectorAspect <float>

   :returns: float

.. object:: objectTemplate.projectorFar <float>

   :returns: float

.. object:: objectTemplate.projectorFov <float>

   :returns: float

.. object:: objectTemplate.projectorNear <float>

   :returns: float

.. object:: objectTemplate.projectorTexture <std::string>

   :returns: std::string

.. object:: objectTemplate.propRotAxis <int>

   :returns: int

.. object:: objectTemplate.pureRotational <bool>

   :returns: bool

.. object:: objectTemplate.QualityLevel <std::string>

   :returns: std::string

.. object:: objectTemplate.radialDirection <float>

   :returns: float

.. object:: objectTemplate.radio.destroyedMessage <std::string>

   :returns: std::string

.. object:: objectTemplate.radio.failMessage <std::string>

   :returns: std::string

.. object:: objectTemplate.radio.repairedMessage <std::string>

   :returns: std::string

.. object:: objectTemplate.radio.spottedMessage <std::string>

   :returns: std::string

.. object:: objectTemplate.radio.useMessage <std::string>

   :returns: std::string

.. object:: objectTemplate.radius <float>

   :returns: float

.. object:: objectTemplate.radiusOffset <Vec3>

   :returns: Vec3

.. object:: objectTemplate.ragdollLandedDelay <float>

   :returns: float

.. object:: objectTemplate.randomAgeFactor <RandomDistribution>

   :returns: RandomDistribution

.. object:: objectTemplate.randomColorIntensity <float>

   :returns: float

.. object:: objectTemplate.randomDirectionAngle <Vec3>

   :returns: Vec3

.. object:: objectTemplate.randomIntensity <float>

   :returns: float

.. object:: objectTemplate.randomizeGeomPart <bool>

   :returns: bool

.. object:: objectTemplate.randomRadialDirection <float>

   :returns: float

.. object:: objectTemplate.randomRotation <float>

   :returns: float

.. object:: objectTemplate.randomRotation <Vec3>

   :returns: Vec3

.. object:: objectTemplate.randomRotationSpeed <Vec3>

   :returns: Vec3

.. object:: objectTemplate.randomRotationSpeed <float>

   :returns: float

.. object:: objectTemplate.randomSize <float>

   :returns: float

.. object:: objectTemplate.randomSpeed <float>

   :returns: float

.. object:: objectTemplate.randomTimeToLive <float>

   :returns: float

.. object:: objectTemplate.rcType <RemoteControlledObjectType>

   :returns: RemoteControlledObjectType

.. object:: objectTemplate.readBinary <std::string>

   :returns: void

.. object:: objectTemplate.recoil.cameraRecoilSize <float>

   :returns: float

.. object:: objectTemplate.recoil.cameraRecoilSpeed <float>

   :returns: float

.. object:: objectTemplate.recoil.goBackOnRecoil <bool>

   :returns: bool

.. object:: objectTemplate.recoil.hasRecoilForce <bool>

   :returns: bool

.. object:: objectTemplate.recoil.recoilForce <float>

   :returns: float

.. object:: objectTemplate.recoil.recoilForceLeftRight <RandomDistribution>

   :returns: RandomDistribution

.. object:: objectTemplate.recoil.recoilForceUp <RandomDistribution>

   :returns: RandomDistribution

.. object:: objectTemplate.recoil.recoilGraphExponent <float>

   :returns: float

.. object:: objectTemplate.recoil.recoilGraphFrameCount <int>

   :returns: int

.. object:: objectTemplate.recoil.recoilGraphTotalMovement <float>

   :returns: float

.. object:: objectTemplate.recoil.recoilSize <float>

   :returns: float

.. object:: objectTemplate.recoil.recoilSpeed <float>

   :returns: float

.. object:: objectTemplate.recoil.recoilSpeedGB <float>

   :returns: float

.. object:: objectTemplate.recoil.zoomModifier <float>

   :returns: float

.. object:: objectTemplate.refillAmmoSpeed <float>

   :returns: float

.. object:: objectTemplate.regulatePitch <Vec2>

   :returns: Vec2

.. object:: objectTemplate.regulatePitchInput <io::PlayerInputMap>

   :returns: io::PlayerInputMap

.. object:: objectTemplate.regulateRoll <Vec2>

   :returns: Vec2

.. object:: objectTemplate.regulateRollInput <io::PlayerInputMap>

   :returns: io::PlayerInputMap

.. object:: objectTemplate.regulateToLift <float>

   :returns: float

.. object:: objectTemplate.regulateVerticalPos <Vec2>

   :returns: Vec2

.. object:: objectTemplate.regulateVerticalPosInput <io::PlayerInputMap>

   :returns: io::PlayerInputMap

.. object:: objectTemplate.regulateYaw <Vec2>

   :returns: Vec2

.. object:: objectTemplate.regulateYawInput <io::PlayerInputMap>

   :returns: io::PlayerInputMap

   - In the effects :file:`.tweak` when creating an effect
   - Allows an effect template to be used with custom settings.

.. object:: objectTemplate.regWhenMinInput <float>

   :returns: float

.. object:: objectTemplate.relativePositionInDof <RandomDistribution>

   :returns: RandomDistribution

.. object:: objectTemplate.relativePositionInRight <RandomDistribution>

   :returns: RandomDistribution

.. object:: objectTemplate.relativePositionInUp <RandomDistribution>

   :returns: RandomDistribution

.. object:: objectTemplate.relativePositionOffset <Vec3>

   :returns: Vec3

.. object:: objectTemplate.rememberExcessInput <bool>

   :returns: bool

.. object:: objectTemplate.remoteEngineInput <int>

   :returns: int

.. object:: objectTemplate.removeTemplate <int>

   :returns: void

.. object:: objectTemplate.replaceItem <std::string>

   :returns: void

   In the :file:`.con` and :file:`.con`

.. object:: objectTemplate.respawnDelay <float>

   :returns: float

   In the :file:`.con` and :file:`.con`

.. object:: objectTemplate.restoreRotationOnExit <bool>

   :returns: bool

.. object:: objectTemplate.restoreSpeed <float>

   :returns: float

.. object:: objectTemplate.reverbLevel <float>

   :returns: float

.. object:: objectTemplate.ropeScaleFactor <float>

   :returns: float

.. object:: objectTemplate.rotateAsAnimatedUV <bool>

   :returns: bool

.. object:: objectTemplate.rotateAsAnimatedUVObject <std::string>

   :returns: std::string

.. object:: objectTemplate.rotateAsAnimatedUVReverse <bool>

   :returns: bool

.. object:: objectTemplate.rotateUV <bool>

   :returns: bool

.. object:: objectTemplate.rotation <float>

   :returns: float

.. object:: objectTemplate.rotationalForce <Vec3>

   :returns: Vec3

.. object:: objectTemplate.rotationalSpeedInDof <RandomDistribution>

   :returns: RandomDistribution

.. object:: objectTemplate.rotationalSpeedInRight <RandomDistribution>

   :returns: RandomDistribution

.. object:: objectTemplate.rotationalSpeedInUp <RandomDistribution>

   :returns: RandomDistribution

.. object:: objectTemplate.rotationAxle <int>

   :returns: int

.. object:: objectTemplate.rotationGraph <Vec4>

   :returns: Vec4

.. object:: objectTemplate.rotationSpeed <Vec3>

   :returns: Vec3

.. object:: objectTemplate.rotationSpeed <float>

   :returns: float

.. object:: objectTemplate.rotationSpeedMod <float>

   :returns: float

.. object:: objectTemplate.rotationSpeedModBlur <float>

   :returns: float

.. object:: ObjectTemplate.save <world::IObjectTemplate_ptrproxy>

   :returns: bool

.. object:: ObjectTemplate.saveAll

   :returns: bool

.. object:: objectTemplate.saveInSeparateFile <bool>

   :returns: bool

.. object:: objectTemplate.scale <Vec3>

   :returns: Vec3

.. object:: objectTemplate.seatAnimationSystem <std::string>

   :returns: std::string

   - In Vehicles :file:`.tweak`
   - Defines the location of the :file:`.inc` animation file for the seat.
   - Example: :file:`Passenger.inc`

.. object:: objectTemplate.seatInformation <std::string Vec3 Vec3>

   :returns: void

.. object:: objectTemplate.seatLeftRotationLimit <float>

   :returns: float

.. object:: objectTemplate.seatParent <std::string>

   :returns: std::string

.. object:: objectTemplate.seatPosition <Vec3>

   :returns: Vec3

.. object:: objectTemplate.seatRightRotationLimit <float>

   :returns: float

.. object:: objectTemplate.seatRotation <Vec3>

   :returns: Vec3

   - In Vehicles :file:`.tweak`
   - Allows the PCO to be rotated.
   - Uses X/Y/Z.
   - Relevant to Seat X Y Z Arrow.
   - See BF2Editor Vehicle for more info.
   - For example -10/0/0 wil rotate the player backwards.

.. object:: objectTemplate.secondaryProjectileTemplate <std::string>

   :returns: std::string

.. object:: objectTemplate.seek.directionBonus <float>

   :returns: float

.. object:: objectTemplate.seek.maxAngleLock <float>

   :returns: float

.. object:: objectTemplate.seek.maxDistLock <float>

   :returns: float

.. object:: objectTemplate.seek.reLockTime <float>

   :returns: float

.. object:: objectTemplate.seek.targetType <TargetType>

   :returns: TargetType

.. object:: objectTemplate.seek.trackingDelay <float>

   :returns: float

.. object:: objectTemplate.selfLights <bool>

   :returns: bool

.. object:: objectTemplate.selfShadowIntensity <float>

   :returns: float

.. object:: objectTemplate.selfShadows <bool>

   :returns: bool

.. object:: objectTemplate.setActiveTemplate <int>

   :returns: void

.. object:: objectTemplate.setAIEnterOnSpawn <bool>

   :returns: void

.. object:: objectTemplate.setAllowSpawnCloseToVehicle <bool>

   :returns: void

.. object:: objectTemplate.setAnimationFrameHeightRelative <float>

   :returns: void

.. object:: objectTemplate.setAnimationFrameWidthRelative <float>

   :returns: void

.. object:: objectTemplate.setAxisFixation <Math::Vec3>

   :returns: void

.. object:: objectTemplate.setCollisionMesh <std::string>

   :returns: void

.. object:: objectTemplate.setEnterOnSpawn <bool>

   :returns: void

.. object:: objectTemplate.setExplodePartAtDestroy <bool>

   :returns: void

.. object:: objectTemplate.setGearRatios <float float float>

   :returns: void

.. object:: objectTemplate.setHasTarget <bool>

   :returns: void

.. object:: objectTemplate.setHealth <int float float>

   :returns: void

.. object:: objectTemplate.setHeatBarType <heatBarType>

   :returns: void

.. object:: objectTemplate.setMinSpawnHeight <float>

   :returns: void

.. object:: objectTemplate.setNumWindows <int>

   :returns: void

.. object:: objectTemplate.setObjectTemplate <int std::string>

   :returns: void

.. object:: objectTemplate.setOnlyForAI <bool>

   :returns: void

.. object:: objectTemplate.setOnlyForHuman <bool>

   :returns: void

.. object:: objectTemplate.setPosition <Math::Vec3 int>

   :returns: void

.. object:: objectTemplate.setPositionalFixation <Math::Vec3>

   :returns: void

.. object:: objectTemplate.setRotation <Math::Vec3 int>

   :returns: void

.. object:: objectTemplate.setScatterSpawnPositions <bool>

   :returns: void

.. object:: objectTemplate.setSkeletonCollisionBone <std::string int Vec3>

   :returns: void

.. object:: objectTemplate.setSoldierExitLocation <Vec3 Vec3>

   :returns: void

.. object:: objectTemplate.setSpawnAsParaTroper <bool>

   :returns: void

.. object:: objectTemplate.setSpawnDelay <float>

   :returns: void

.. object:: objectTemplate.setSpawnPositionOffset <Math::Vec3>

   :returns: void

.. object:: objectTemplate.setSpawnPreventionDelay <float>

   :returns: void

.. object:: objectTemplate.setSpawnRotation <Math::Vec3>

   :returns: void

.. object:: objectTemplate.setTeamGeometry <int std::string>

   :returns: void

.. object:: objectTemplate.setToolTipType <dice::hfe::world::ToolTipType>

   :returns: void

.. object:: objectTemplate.setVehicleType <dice::hfe::world::VehicleType>

   :returns: void

.. object:: objectTemplate.shadowIntensity <float>

   :returns: float

.. object:: objectTemplate.shakeFactor <float>

   :returns: float

.. object:: objectTemplate.sharedStorageSize <float>

   :returns: float

.. object:: objectTemplate.showInFirstPerson <bool>

   :returns: bool

.. object:: objectTemplate.showInThirdPerson <bool>

   :returns: bool

.. object:: objectTemplate.showOnMinimap <bool>

   :returns: bool

.. object:: objectTemplate.signalTriggerId <int>

   :returns: int

.. object:: objectTemplate.sinkingSpeedMod <float>

   :returns: float

.. object:: objectTemplate.size <float>

   :returns: float

.. object:: objectTemplate.size <RandomDistribution>

   :returns: RandomDistribution

.. object:: objectTemplate.sizeGraph <Vec4>

   :returns: Vec4

.. object:: objectTemplate.sizeModifier <Vec3>

   :returns: Vec3

.. object:: objectTemplate.sizeModifierX <float>

   :returns: float

.. object:: objectTemplate.sizeModifierY <float>

   :returns: float

.. object:: objectTemplate.sizeModifierZ <float>

   :returns: float

.. object:: objectTemplate.sizeOverTime <OverTimeDistribution>

   :returns: OverTimeDistribution

.. object:: objectTemplate.skeleton <std::string>

   :returns: void

.. object:: objectTemplate.skeleton1P <std::string>

   :returns: void

.. object:: objectTemplate.skeleton3P <std::string>

   :returns: void

.. object:: objectTemplate.snapToZeroOnNoInput <bool>

   :returns: bool

.. object:: objectTemplate.softness <float>

   :returns: float

.. object:: objectTemplate.soldierExitPosition <Vec3>

   :returns: Vec3

.. object:: objectTemplate.soldierExitRotation <Vec3>

   :returns: Vec3

.. object:: objectTemplate.sound.maxSoundsPerBurst <int>

   :returns: int

.. object:: objectTemplate.sound.noisy <bool>

   :returns: bool

.. object:: objectTemplate.soundFilename <std::string>

   :returns: std::string

.. object:: objectTemplate.soundFilter <std::string>

   :returns: std::string

.. object:: objectTemplate.soundIntensityFromAcceleration <Vec2>

   :returns: Vec2

.. object:: objectTemplate.soundIntensityFromAltitude <Vec2>

   :returns: Vec2

.. object:: objectTemplate.soundIntensityFromEngine <Vec2>

   :returns: Vec2

.. object:: objectTemplate.soundIntensityFromRotationalSpeed <Vec2>

   :returns: Vec2

.. object:: objectTemplate.soundIntensityFromSpeed <Vec2>

   :returns: Vec2

.. object:: objectTemplate.soundIntensityFromSpeedInDof <Vec2>

   :returns: Vec2

.. object:: objectTemplate.soundIntensityRange <Vec2>

   :returns: Vec2

.. object:: objectTemplate.soundIntensityUsed <bool>

   :returns: bool

.. object:: objectTemplate.soundRadius <float>

   :returns: float

.. object:: objectTemplate.spawnDelay <float>

   :returns: void

.. object:: objectTemplate.spawnDelayAtStart <bool>

   :returns: bool

.. object:: objectTemplate.spawnOffset <Vec3>

   :returns: Vec3

.. object:: objectTemplate.speccolor <Vec3ColorFloatIntensity>

   :returns: Vec3ColorFloatIntensity

.. object:: objectTemplate.specialToggleWeaponInput <io::PlayerInputMap>

   :returns: io::PlayerInputMap

.. object:: objectTemplate.speed <float>

   :returns: float

.. object:: objectTemplate.speedFromParticle <float>

   :returns: float

.. object:: objectTemplate.speedFromPhysics <bool>

   :returns: bool

.. object:: objectTemplate.spinWhenNoEngineInAir <float>

   :returns: float

.. object:: objectTemplate.sprintDissipationTime <float>

   :returns: float

.. object:: objectTemplate.sprintFactor <float>

   :returns: float

.. object:: objectTemplate.sprintGear1Dampen <float>

   :returns: float

.. object:: objectTemplate.sprintGear2Dampen <float>

   :returns: float

.. object:: objectTemplate.sprintGear3Dampen <float>

   :returns: float

.. object:: objectTemplate.sprintGear4Dampen <float>

   :returns: float

.. object:: objectTemplate.sprintGear5Dampen <float>

   :returns: float

.. object:: objectTemplate.sprintLimit <float>

   :returns: float

.. object:: objectTemplate.sprintLossAtJump <float>

   :returns: float

.. object:: objectTemplate.sprintRecoverTime <float>

   :returns: float

.. object:: objectTemplate.sprintStaminaDissipationFactor <float>

   :returns: float

.. object:: objectTemplate.startAgeFromAcceleration <Vec2>

   :returns: Vec2

.. object:: objectTemplate.startAgeFromAltitude <Vec2>

   :returns: Vec2

.. object:: objectTemplate.startAgeFromEngine <Vec2>

   :returns: Vec2

.. object:: objectTemplate.startAgeFromRotationalSpeed <Vec2>

   :returns: Vec2

.. object:: objectTemplate.startAgeFromSpeed <Vec2>

   :returns: Vec2

.. object:: objectTemplate.startAgeFromSpeedInDof <Vec2>

   :returns: Vec2

.. object:: objectTemplate.startAgeRange <Vec2>

   :returns: Vec2

.. object:: objectTemplate.startAgeUsed <bool>

   :returns: bool

.. object:: objectTemplate.startAtCreation <bool>

   :returns: bool

.. object:: objectTemplate.startAutoRotateOnEnter <bool>

   :returns: bool

.. object:: objectTemplate.startDelay <float>

   :returns: float

.. object:: objectTemplate.startDistance <float>

   :returns: float

.. object:: objectTemplate.startLodPercentageOfLodDistance <float>

   :returns: float

.. object:: objectTemplate.startOnEffects <int>

   :returns: int

.. object:: objectTemplate.startProbability <float>

   :returns: float

.. object:: objectTemplate.startRotation <RandomDistribution>

   :returns: RandomDistribution

.. object:: objectTemplate.startTeam <int>

   :returns: int

.. object:: objectTemplate.stopOnEffects <int>

   :returns: int

.. object:: objectTemplate.stopType <int>

   :returns: int

.. object:: objectTemplate.strategicObject.3dMapIcon <int>

   :returns: int

.. object:: objectTemplate.strategicObject.destroyedIcon <std::string>

   :returns: std::string

.. object:: objectTemplate.strategicObject.intactIcon <std::string>

   :returns: std::string

.. object:: objectTemplate.strategicObject.isOnePiece <bool>

   :returns: bool

.. object:: objectTemplate.strategicObject.part <int>

   :returns: int

.. object:: objectTemplate.strategicObject.strategicObjectName <std::string>

   :returns: std::string

.. object:: objectTemplate.strength <float>

   :returns: float

.. object:: objectTemplate.supplyGroupId <int>

   :returns: int

.. object:: objectTemplate.supplyGroupNeeded <int int bool>

   :returns: void

.. object:: objectTemplate.supplyValueNeededTeam1 <int>

   :returns: int

.. object:: objectTemplate.supplyValueNeededTeam2 <int>

   :returns: int

.. object:: objectTemplate.supplyValueTeam1 <int>

   :returns: int

.. object:: objectTemplate.supplyValueTeam2 <int>

   :returns: int

.. object:: objectTemplate.supportsEmitter <bool>

   :returns: bool

.. object:: objectTemplate.supportsGlow <bool>

   :returns: bool

.. object:: objectTemplate.supportsPerPixel <bool>

   :returns: bool

.. object:: objectTemplate.supportsPerVertex <bool>

   :returns: bool

.. object:: objectTemplate.target.connectionEffect <std::string>

   :returns: std::string

.. object:: objectTemplate.target.connectionEffectOnlyWhenZoomed <bool>

   :returns: bool

.. object:: objectTemplate.target.disableFireWhenActiveMissile <bool>

   :returns: bool

.. object:: objectTemplate.target.disableGuidanceOnReload <bool>

   :returns: bool

.. object:: objectTemplate.target.lockAngle <float>

   :returns: float

.. object:: objectTemplate.target.lockDelay <float>

   :returns: float

.. object:: objectTemplate.target.loseLockDelay <float>

   :returns: float

.. object:: objectTemplate.target.maxDistance <float>

   :returns: float

.. object:: objectTemplate.target.maxVelocity <float>

   :returns: float

.. object:: objectTemplate.target.minVelocity <float>

   :returns: float

.. object:: objectTemplate.target.onLockChangeToWeapon <bool std::string>

   :returns: void

.. object:: objectTemplate.target.sendVehicleLockWarning <bool>

   :returns: bool

.. object:: objectTemplate.target.setTargetAtMaxDistance <bool>

   :returns: bool

.. object:: objectTemplate.target.targetInput <io::PlayerInputMap>

   :returns: io::PlayerInputMap

.. object:: objectTemplate.target.targetObjectTemplate <std::string>

   :returns: std::string

.. object:: objectTemplate.target.targetSystem <TargetSystem>

   :returns: TargetSystem

.. object:: objectTemplate.target.updateInterval <float>

   :returns: float

.. object:: objectTemplate.target.useCameraDirectionToTarget <bool>

   :returns: bool

.. object:: objectTemplate.target.useDynamicVelocity <bool>

   :returns: bool

.. object:: objectTemplate.target.velocityModifier <float>

   :returns: float

.. object:: objectTemplate.targetType <TargetType>

   :returns: TargetType

.. object:: objectTemplate.team <int>

   :returns: int

.. object:: objectTemplate.team <U32>

   :returns: U32

.. object:: objectTemplate.team <int>

   :returns: void

.. object:: objectTemplate.teamChange <bool>

   :returns: bool

.. object:: objectTemplate.teamFromClosestCP <bool>

   :returns: bool

.. object:: objectTemplate.teamOnVehicle <bool>

   :returns: bool

.. object:: objectTemplate.template <std::string>

   :returns: std::string

.. object:: objectTemplate.templateHasBeenUsed <bool>

   :returns: bool

.. object:: objectTemplate.textureName <std::string>

   :returns: std::string

.. object:: objectTemplate.textureOffsetVelocity <float>

   :returns: float

.. object:: objectTemplate.textureTileFactor <float>

   :returns: float

.. object:: objectTemplate.throwStrength <float>

   :returns: float

.. object:: objectTemplate.throwStrength2 <float>

   :returns: float

.. object:: objectTemplate.Timeout <float>

   :returns: float

.. object:: objectTemplate.timeToGetControl <float>

   :returns: float

.. object:: objectTemplate.timeToLive <RandomDistribution>

   :returns: RandomDistribution

.. object:: objectTemplate.timeToLive <float>

   :returns: float

.. object:: objectTemplate.timeToLiveAfterDeath <float>

   :returns: float

.. object:: objectTemplate.timeToLoseControl <float>

   :returns: float

.. object:: objectTemplate.timeToRemoveTK <float>

   :returns: float

.. object:: objectTemplate.toggleMouseLook <bool>

   :returns: bool

.. object:: objectTemplate.toggleWeapon <bool>

   :returns: bool

.. object:: objectTemplate.tolerance <float>

   :returns: float

.. object:: objectTemplate.torque <float>

   :returns: float

.. object:: objectTemplate.tracerConvergeDistance <float>

   :returns: float

   - Used in Projectiles (Weapons)
   - At what distance the tracers (which start from the gunbarrel) and the projectile which start from the camera converges.
   - Only relevant if ``FireInCameraDof`` is checked.

.. object:: objectTemplate.tracerInterval <int>

   :returns: int

   - Used in Projectiles (Weapons)
   - Set one for tracer on every shot, 2 for every other, and so on.

.. object:: objectTemplate.tracerScaler <float>

   :returns: float

   - Used in Projectiles (Weapons)
   - How long the tracer effect will be as default.

.. object:: objectTemplate.tracerSizeModifier <float>

   :returns: float

   - Used in Projectiles (Weapons)
   - How fat the tracer will be.

.. object:: objectTemplate.tracerTemplate <std::string>

   :returns: std::string

.. object:: objectTemplate.trackTurnAcceleration <float>

   :returns: float

.. object:: objectTemplate.trackTurnHighAmplitude <float>

   :returns: float

.. object:: objectTemplate.trackTurnHighOffset <float>

   :returns: float

.. object:: objectTemplate.trackTurnLowAmplitude <float>

   :returns: float

.. object:: objectTemplate.trackTurnLowOffset <float>

   :returns: float

.. object:: objectTemplate.trackTurnSpeed <float>

   :returns: float

.. object:: objectTemplate.trailEffectTemplate <std::string>

   :returns: std::string

.. object:: objectTemplate.Transparency <RandomDistribution>

   :returns: RandomDistribution

.. object:: objectTemplate.transparencyGraph <Vec4>

   :returns: Vec4

.. object:: objectTemplate.treeCollisionDiameter <float>

   :returns: float

.. object:: objectTemplate.triggerForEachActivatingPlayer <bool>

   :returns: bool

.. object:: objectTemplate.triggerId <int>

   :returns: int

.. object:: objectTemplate.triggerRadius <float>

   :returns: float

.. object:: objectTemplate.turnVelocity <float>

   :returns: float

.. object:: ObjectTemplate.type <world::IObjectTemplate_ptrproxy>

   :returns: std::string

.. object:: objectTemplate.type <int>

   :returns: int

.. object:: objectTemplate.uavVehicleFlightHeight <float>

   :returns: float

.. object:: objectTemplate.uavVehicleRadius <float>

   :returns: float

.. object:: objectTemplate.uavVehicleSampleResolution <float>

   :returns: float

.. object:: objectTemplate.uavVehicleSpeed <float>

   :returns: float

.. object:: objectTemplate.uavVehicleTemplate <std::string>

   :returns: std::string

.. object:: objectTemplate.unableToChangeTeam <bool>

   :returns: bool

.. object:: objectTemplate.unlockIndex <int>

   :returns: int

.. object:: objectTemplate.unlockLevel <int>

   :returns: int

.. object:: ObjectTemplate.update <world::IObjectTemplate_ptrproxy>

   :returns: void

.. object:: ObjectTemplate.updateAll

   :returns: void

.. object:: objectTemplate.upDropBoost <float>

   :returns: float

.. object:: objectTemplate.upThrowBoost <float>

   :returns: float

.. object:: objectTemplate.upThrowBoost2 <float>

   :returns: float

.. object:: objectTemplate.useAbsoluteDirection <bool>

   :returns: bool

.. object:: objectTemplate.useButtonRadius <float>

   :returns: float

.. object:: objectTemplate.useCameraOrientation <bool>

   :returns: bool

.. object:: objectTemplate.usedByAi <bool>

   :returns: bool

.. object:: objectTemplate.useDeAcceleration <bool>

   :returns: bool

.. object:: objectTemplate.usedOnTransparentMaterials <bool>

   :returns: bool

.. object:: objectTemplate.usedOnTransparentSurface <bool>

   :returns: bool

.. object:: objectTemplate.useGeomPart <int>

   :returns: int

.. object:: objectTemplate.useProjectileCamera <bool>

   :returns: bool

.. object:: objectTemplate.vehicleCameraShake <CameraShakeTriggers>

   :returns: CameraShakeTriggers

.. object:: objectTemplate.vehicleCategory <dice::hfe::world::VehicleCategory>

   :returns: dice::hfe::world::VehicleCategory

.. object:: objectTemplate.vehicleFov <float>

   :returns: float

.. object:: objectTemplate.vehicleHud.AbilityIcon <std::string>

   :returns: std::string

.. object:: objectTemplate.vehicleHud.addAbilityIcon <std::string>

   :returns: void

.. object:: objectTemplate.vehicleHud.addShowOnCamMode <int>

   :returns: void

.. object:: objectTemplate.vehicleHud.addVehicleIcon <std::string>

   :returns: void

.. object:: objectTemplate.vehicleHud.disableOnSprint <bool>

   :returns: bool

.. object:: objectTemplate.vehicleHud.displaySelectionOnEnter <bool>

   :returns: bool

.. object:: objectTemplate.vehicleHud.enablePostProcessingOnGuiIndex <bool>

   :returns: bool

.. object:: objectTemplate.vehicleHud.getShowOnCamMode <int>

   :returns: bool

.. object:: objectTemplate.vehicleHud.guiIndex <int>

   :returns: int

   - Vehicles and Weapons :file:`.tweak`
   - Defines the Vehicle General User Inferface Index to use like the Blackhawk green HUD.
   - Gui Index is located in the :file:`.con`\ s of :file:`menu\\HUD\\HudSetup\\Vehicles`

.. object:: objectTemplate.vehicleHud.hasTurretIcon <bool>

   :returns: bool

.. object:: objectTemplate.vehicleHud.hudName <std::string>

   :returns: std::string

.. object:: objectTemplate.vehicleHud.injurySound <std::string>

   :returns: std::string

.. object:: objectTemplate.vehicleHud.isCoDriver <bool>

   :returns: bool

.. object:: objectTemplate.vehicleHud.maxClimbSpeed <int>

   :returns: int

.. object:: objectTemplate.vehicleHud.miniMapIcon <std::string>

   :returns: std::string

.. object:: objectTemplate.vehicleHud.miniMapIconLeaderSize <std::string>

   :returns: std::string

.. object:: objectTemplate.vehicleHud.miniMapIconSize <int>

   :returns: int

.. object:: objectTemplate.vehicleHud.pantingSound <std::string>

   :returns: std::string

.. object:: objectTemplate.vehicleHud.showCrossHair <bool>

   :returns: bool

.. object:: objectTemplate.vehicleHud.showInfo <bool>

   :returns: bool

.. object:: objectTemplate.vehicleHud.showOnCamMode <int>

   :returns: int

.. object:: objectTemplate.vehicleHud.spottedIcon <std::string>

   :returns: std::string

.. object:: objectTemplate.vehicleHud.spottedIconSize <int>

   :returns: int

.. object:: objectTemplate.vehicleHud.standardHelpEnabled <bool>

   :returns: bool

.. object:: objectTemplate.vehicleHud.typeIcon <std::string>

   :returns: std::string

.. object:: objectTemplate.vehicleHud.useChildHud <bool>

   :returns: bool

.. object:: objectTemplate.vehicleHud.usePlayerIcon <bool>

   :returns: bool

.. object:: objectTemplate.vehicleHud.useSelectionIcons <bool>

   :returns: bool

.. object:: objectTemplate.vehicleHud.useVehicleCommRose <bool>

   :returns: bool

.. object:: objectTemplate.vehicleHud.vehicleIcon <std::string>

   :returns: std::string

.. object:: objectTemplate.vehicleHud.vehicleIconPos <Vec2>

   :returns: Vec2

.. object:: objectTemplate.vehicleHud.vehicleType <int>

   :returns: int

.. object:: objectTemplate.velocity <float>

   :returns: float

   - Used in ``GenericFirearms`` (Weapons, Projectiles)
   - The speed of the projectile measured in Rate of Fire (ROF)
   - Lower ROF are affected by gravity/bullet drop while higher ones fire with lower bullet drop

.. object:: objectTemplate.visibleOn3dMap <bool>

   :returns: bool

.. object:: objectTemplate.volume <float>

   :returns: float

   The loudness of the sound.

.. object:: objectTemplate.volumeEnvelope <std::string>

   :returns: std::string

.. object:: objectTemplate.volumeGroup <int>

   :returns: int

.. object:: objectTemplate.warningHud.firstWarningSound <std::string>

   :returns: std::string

   - Used in Vehicle :file:`.tweak`
   - Defines the 1st warning sound when getting locked onto.
   - Uses the file path pointing to a :file:`.wav` or an :file:`.wav` file along with usual sound configuration code. *Beep Beep Beep*

.. object:: objectTemplate.warningHud.secondWarningSound <std::string>

   :returns: std::string

   - Used in Vehicle :file:`.tweak`
   - Defines the 2nd warning sound when getting locked onto.
   - Uses the file path pointing to a :file:`.wav` or an :file:`.wav` file along with usual sound configuration code. *Beeeeeeeeeeep*

.. object:: objectTemplate.warningHud.warningIcon <std::string>

   :returns: std::string

   - Used in Vehicle :file:`.tweak`
   - Defines the location of the warning icon.
   - Example: ``ObjectTemplate.WarningHud.warningIcon Ingame\GeneralIcons\Action_Icons\mylaserlockicon.tga``

.. object:: objectTemplate.warningHud.warningType <int>

   :returns: int

.. object:: objectTemplate.waterHeight <float>

   :returns: float

.. object:: objectTemplate.waterSurfaceOffset <float>

   :returns: float

.. object:: objectTemplate.weaponHud.addShowOnCamMode <int>

   :returns: void

.. object:: objectTemplate.weaponHud.altCrosshairIcon <std::string>

   :returns: std::string

.. object:: objectTemplate.weaponHud.altGuiIndex <int>

   :returns: int

.. object:: objectTemplate.weaponHud.altWeaponIcon <std::string>

   :returns: std::string

.. object:: objectTemplate.weaponHud.ammoBarBackIcon <std::string>

   :returns: std::string

.. object:: objectTemplate.weaponHud.ammoBarFrontIcon <std::string>

   :returns: std::string

.. object:: objectTemplate.weaponHud.ammoIcon <std::string>

   :returns: std::string

.. object:: objectTemplate.weaponHud.clipIcon <std::string>

   :returns: std::string

.. object:: objectTemplate.weaponHud.crosshairIcon <std::string>

   :returns: std::string

.. object:: objectTemplate.weaponHud.crosshairIconSize <int>

   :returns: int

.. object:: objectTemplate.weaponHud.deviationFactor <int>

   :returns: int

.. object:: objectTemplate.weaponHud.disableOnSprint <bool>

   :returns: bool

   - Used in Weapons and Vehicle :file:`.tweak`

.. object:: objectTemplate.weaponHud.displaySelectOnActivation <bool>

   :returns: bool

.. object:: objectTemplate.weaponHud.enableMouse <bool>

   :returns: bool

.. object:: objectTemplate.weaponHud.enablePostProcessingOnGuiIndex <int>

   :returns: int

   - Used in Weapons and Vehicle :file:`.tweak`
   - Makes the GuiIndex have a black and white effect
   - Use with all ``objectTemplate.postProcess.tv`` code to adjust the TV effect

.. object:: objectTemplate.weaponHud.firstLockSound <std::string>

   :returns: std::string

   The first lock sound that plays when there is a lock in progress on the jet

.. object:: objectTemplate.weaponHud.getShowOnCamMode <int>

   :returns: bool

.. object:: objectTemplate.weaponHud.guiIndex <int>

   :returns: int

   - Used in Weapons and Vehicle :file:`.tweak`
   - Defines the Weapon General User Inferface Index to use like the repair bar
   - Gui Index is located in the :file:`.con`\ s of :file:`menu\\HUD\\HudSetup\\Vehicles`

.. object:: objectTemplate.weaponHud.hasFireRate <bool>

   :returns: bool

   Used in Weapons and Vehicle :file:`.tweak`

.. object:: objectTemplate.weaponHud.hasMag <bool>

   :returns: bool

.. object:: objectTemplate.weaponHud.hasRangeFinder <bool>

   :returns: bool

.. object:: objectTemplate.weaponHud.hudName <std::string>

   :returns: std::string

.. object:: objectTemplate.weaponHud.maxVisualDeviation <int>

   :returns: int

.. object:: objectTemplate.weaponHud.minVisualDeviation <int>

   :returns: int

.. object:: objectTemplate.weaponHud.overheatSound <std::string>

   :returns: std::string

   - Used in Weapons and Vehicle :file:`.tweak`
   - For the overheat sound. Adding it makes the engine reference the std::string defined with MenuSound.con.

     - Usually it's ``S_Weapon_Handheld_Overheat``
     - ``S_Vehicle_Handheld_Overheat`` but can be anything and custom ones can be used if needed

.. object:: objectTemplate.weaponHud.secondLockSound <std::string>

   :returns: std::string

   - Used in Weapons and Vehicle :file:`.tweak`
   - The second lock sound that plays when the lock has been set

.. object:: objectTemplate.weaponHud.selectIcon <std::string>

   :returns: std::string

.. object:: objectTemplate.weaponHud.showAmmo <bool>

   :returns: bool

.. object:: objectTemplate.weaponHud.ShowClips <bool>

   :returns: bool

.. object:: objectTemplate.weaponHud.showInfo <bool>

   :returns: bool

.. object:: objectTemplate.weaponHud.showOnCamMode <int>

   :returns: int

.. object:: objectTemplate.weaponHud.specialAbilityIcon <std::string>

   :returns: std::string

.. object:: objectTemplate.weaponHud.switchGuiOnCamera <bool>

   :returns: bool

.. object:: objectTemplate.weaponHud.weaponIcon <std::string>

   :returns: std::string

.. object:: objectTemplate.weaponType <int>

   :returns: int

.. object:: objectTemplate.widnBlowTime <float>

   :returns: float

.. object:: objectTemplate.windAffectionFactor <float>

   :returns: float

.. object:: objectTemplate.windAgingFactor <float>

   :returns: float

.. object:: objectTemplate.windBlowTime <float>

   :returns: float

.. object:: objectTemplate.windDirection <Vec3>

   :returns: Vec3

.. object:: objectTemplate.windFalloff <float>

   :returns: float

.. object:: objectTemplate.windIsDynamic <bool>

   :returns: bool

.. object:: objectTemplate.windowSizeVector <Vec3>

   :returns: Vec3

   Used in Projectiles, Vehicles, Effect

.. object:: objectTemplate.windRadialFalloff <float>

   :returns: float

.. object:: objectTemplate.windSpeed <float>

   :returns: float

.. object:: objectTemplate.windSpeedAgeDistance <float>

   :returns: float

.. object:: objectTemplate.windType <std::string>

   :returns: std::string

.. object:: objectTemplate.wingLift <float>

   :returns: float

   - Planes and Helis
   - How much speed will affect object lifting on control surface.

.. object:: objectTemplate.wingToRegulatorRatio <float>

   :returns: float

.. object:: objectTemplate.workOnSoldiers <bool>

   :returns: bool

   - Supply Objects
   - Allows the soldier to receive HP/Ammo depending on the type of supply set

.. object:: objectTemplate.workOnVehicles <bool>

   :returns: bool

   - Supply Objects
   - Allows the vehicle to receive HP/Ammo depending on the type of supply set

.. object:: objectTemplate.worldFOV <float>

   :returns: float

.. object:: objectTemplate.writeBinary <std::string>

   :returns: void

.. object:: objectTemplate.writeZ <bool>

   :returns: bool

.. object:: objectTemplate.yawSpeed <float>

   :returns: float

.. object:: objectTemplate.ziplineSoldierHeight <float>

   :returns: float

.. object:: objectTemplate.zoom.addZoomFactor <float>

   :returns: void

.. object:: objectTemplate.zoom.allowUntoggledFire <bool>

   :returns: bool

.. object:: objectTemplate.zoom.changeCameraId <int>

   :returns: int

.. object:: objectTemplate.zoom.changeCameraViewMode <CameraViewMode>

   :returns: CameraViewMode

.. object:: objectTemplate.zoom.changeFovDelay <float>

   :returns: float

.. object:: objectTemplate.zoom.disableMuzzleWhenZoomed <bool>

   :returns: bool

.. object:: objectTemplate.zoom.mouseSpeedMod <float>

   :returns: float

.. object:: objectTemplate.zoom.onlyZoomWhenProne <bool>

   :returns: bool

.. object:: objectTemplate.zoom.startCameraId <int>

   :returns: int

.. object:: objectTemplate.zoom.startCameraViewMode <CameraViewMode>

   :returns: CameraViewMode

.. object:: objectTemplate.zoom.useProjectileCamera <bool>

   :returns: bool

.. object:: objectTemplate.zoom.zoomDelay <float>

   :returns: float

.. object:: objectTemplate.zoom.zoomInput <io::PlayerInputMap>

   :returns: io::PlayerInputMap

.. object:: objectTemplate.zoom.zoomLod <int>

   :returns: int

.. object:: objectTemplate.zoom.zoomOutAfterFire <bool>

   :returns: bool

.. object:: objectTemplate.zRotation <RandomDistribution>

   :returns: RandomDistribution

.. object:: objectTemplate.zRotationSnap <float>

   :returns: float
