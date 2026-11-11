
Manual Ambient Object Configuration
===================================

This guide describes how to manually configure and correct Ambient Objects. It is recommended to first load the level in the BF2 Editor and review the debugger logs.

Ambient objects consist of three mandatory elements, which must be created in the following order:

#. **Trigger**: A player-activated radius. Within this radius, player actions (e.g., firing, moving, waiting, or an explosion) activate an ambient effect. Triggers appear blue in the editor.
#. **Ambient Effect Area**: Defines the properties of the effect linked to the Trigger. The trigger name must include the suffix ``_AmbientEffect``. Ambient Effect Areas are marked red in the editor.
#. **Ambient Sounds**: Defines atmospheric sounds that play across the entire map or in specific locations. Ambient Sounds appear green in the editor.

Trigger
-------

.. describe:: ObjectTemplate.create Trigger [Object] -> object.Create

   This command defines the Trigger ID and the properties of the soldier-activated trigger.

.. describe:: objectTemplate.triggerId (int -> int)

   The unique identification number for the trigger within the game. This must be defined for both the Trigger and the ``[Object]_AmbientEffect``. The same ID can be used for multiple ``_AmbientEffect`` instances to activate different effects, provided the naming convention is consistent (e.g., ``Sandstorm_AmbientObject_1``, ``Sandstorm_AmbientObject_2``).

.. describe:: objectTemplate.radius (float -> float)

   Sets the spherical area (dome) that detects player interaction and activates the ``AmbientEffectArea``. This area can be visualized in the BF2 Editor.

.. describe:: objectTemplate.events (int -> int)

   Specifies the trigger type. Enter the corresponding number in the ``[]`` section of this parameter. Refer to the Trigger Types section for details.

.. describe:: objectTemplate.averageTimeBetweenTests (float -> float)

   Determines how long the effect remains active. This is primarily used for sound effects (e.g., bird chirps). The value must be at least ``1``.

.. describe:: objectTemplate.chance (float -> float)

   Sets the probability of the effect playing. The value ranges from ``0`` (never plays) to ``1`` (always plays). For example, ``0.5`` provides a 50% chance.

.. describe:: objectTemplate.minimumTimeBetweenTriggering (float -> float)

   Specifies the minimum number of seconds required before the effect can be triggered again after playing.

.. describe:: objectTemplate.create

   Defines the effect's position for both the ``Trigger`` and the ``AmbientEffectArea``. Use the BF2 Editor to set this position accurately.

Trigger Types
-------------

There are four trigger types. Add the corresponding number in the ``objectTemplate.events`` parameter:

:Time: `1` (activates based on a defined time, independent of ``ObjectTemplate.time``).
:Fire: `2` (activates when a player within the radius fires a weapon).
:Move: `4` (activates when a player moves into the radius).
:Explosion: `8` (activates when an explosion occurs within the radius).

Combine multiple trigger types by adding their values (e.g., ``14`` for Time and Move, or ``128`` for Time, Fire, and Explosion).

Once the Trigger is defined, create the object using ``Object.create`` with the same name to place it on the map. This utilizes the absolute position, rotation, and the intended layer.

.. code-block:: text
   :caption: Example Trigger Configuration

   rem [TriggerTemplate: Trigger_birds1]
   rem *********** TriggerTrigger ***********
   rem [TriggerTemplate: Trigger_birds1]
   ObjectTemplate.create Trigger Trigger_birds1
   ObjectTemplate.activeSafe Trigger Trigger_birds1
   ObjectTemplate.modifiedByUser esj
   ObjectTemplate.isNotSaveable 1
   ObjectTemplate.hasMobilePhysics 0
   ObjectTemplate.triggerId 1
   ObjectTemplate.radius 30
   ObjectTemplate.events 10
   ObjectTemplate.averageTimeBetweenTests 1
   ObjectTemplate.chance 0.5
   ObjectTemplate.minimumTimeBetweenTriggering 30

      rem [Trigger: Trigger_birds1]
      Object.create Trigger_birds1
      Object.absolutePosition 82.964/153.389/-19.101
      Object.rotation 0.000/0.000/0.000
      Object.layer 1

AmbientEffectArea
-----------------

.. describe:: `ObjectTemplate.create AmbientEffectArea [Object]_AmbientEffect_# (Where # is the sequence number)`, `object.Create`

   The ``AmbientEffectArea`` defines the effect's radius, the specific effect used, and its properties.

.. describe:: objectTemplate.numNetworkedEffects

   Used for triggers that activate multiple effects simultaneously.

.. describe:: objectTemplate.projectOnHeightmap

   Set to ``1`` to make the effect appear to originate from the ground. If set to ``0`` (default), the effect plays relative to its defined position.

.. describe:: objectTemplate.playAtEventPosition

   Self-explanatory.

.. describe:: objectTemplate.playAtPlayerPosition

   Self-explanatory.

.. describe:: objectTemplate.radius (float -> float)

   Defines the spherical boundary within which the effect will cease.

.. describe:: objectTemplate.linkedEffectContainer (std::string -> std::string)

   Specifies the effect that plays when a soldier enters the ``AmbientEffectArea`` radius (e.g., ``e_dAmb_bird``).

.. note::

   For ``AmbientEffects`` to function correctly, the ``_AmbientEffect`` suffix must be added to the object name. The most efficient method is to search for the effect and replace it with the effect name followed by ``_AmbientEffect``. The ``AmbientEffectArea`` must share the same Trigger ID as the parent Trigger.

After defining the ``AmbientEffectArea``, create the object using ``Object.create`` with the same name to place it on the map. You may use the same coordinates as the Trigger.

.. code-block:: text
   :caption: Example AmbientEffectArea Configuration

   rem ********** AmbientEffectArea **********
   rem TriggerID must match the TriggerTrigger
   rem [AmbientEffectAreaTemplate: Trigger_birds1_AmbientEffect_1]
   ObjectTemplate.create AmbientEffectArea Trigger_birds1_AmbientEffect_1
   ObjectTemplate.activeSafe AmbientEffectArea Trigger_birds1_AmbientEffect_1
   ObjectTemplate.modifiedByUser esj
   ObjectTemplate.isNotSaveable 1
   ObjectTemplate.hasMobilePhysics 0
   ObjectTemplate.radius 2
   ObjectTemplate.triggerId 1
   ObjectTemplate.numNetworkedEffects 1
   ObjectTemplate.projectOnHeightmap 0
   ObjectTemplate.linkedEffectContainer e_dAmb_bird

      rem [AmbientEffectArea: Trigger_birds1_AmbientEffect_1]
      Object.create Trigger_birds1_AmbientEffect_1
      Object.absolutePosition 83.191/159.486/-19.643
      Object.rotation 0.000/0.000/0.000
      Object.layer 1

AmbientSounds
-------------

.. describe:: `ObjectTemplate.create Sound S_`, `ObjectTemplate.activeSafe Sound S_`, `Sound.addTrigger S_`, `Object.create S_`

   Ambient Sounds define atmospheric sounds that play across the entire map or in specific locations.

.. describe:: objectTemplate.lowSamples (int -> int)

   Refers to the low sample audio bitrate; do not alter this value.

.. describe:: objectTemplate.mediumSamples (int -> int)

   Refers to the medium sample audio bitrate; do not alter this value.

.. describe:: objectTemplate.soundFilename (std::string -> std::string)

   Specifies the sound file path. Use the BF2 Editor to locate these files.

.. describe:: objectTemplate.loopCount (int -> int)

   Controls the number of sound loops:

   :0: Loops indefinitely.
   :1: Plays once.
   :2: Plays twice.

.. describe:: objectTemplate.is3dSound (bool -> bool)

   Enable this only if the sound file is mono and must play through both speakers. Enabling this for a stereo file will cause the sound to play across the entire map incorrectly.

.. describe:: objectTemplate.volume (float -> float)

   Controls the loudness of the sound.

.. describe:: objectTemplate.pan (float -> float)

   Controls the left-to-right direction of the sound:

   :0: Directs the sound to the left speaker.
   :1: Directs the sound to the right speaker.
   :0.5: (Default) Centers the sound.

.. describe:: objectTemplate.reverbLevel (float -> float)

   Sets the reverberation level between 0 and 1. The default value is 0.

.. describe:: objectTemplate.pitch (float -> float)

   Adjusts the sound's pitch. The default value is 1.

.. describe:: objectTemplate.minDistance (float -> float)

   Sets the minimum distance from the sound's position at which it can be heard. This value must be set for the sound to play.

.. describe:: objectTemplate.soundRadius (float -> float)

   Defines the radius within which the sound begins to play as a player enters. This must be set in conjunction with ``minDistance``.

.. describe:: objectTemplate.stopType (int -> int)

   Defines the stop behavior (0, 1, or 2). It is recommended to use ``0`` for ambient weather sounds and large areas (typically located in ``common/sound/levelambients``). When set to ``0``, the sound will replay and overlap each time a player enters and exits the radius. Use ``1`` for specific ambient effects like chimes, birds, or swamp creeks.

.. describe:: objectTemplate.position (Vec3 -> Vec3)

   Specifies the sound's position. This must match the ``ObjectTemplate.absolutePosition`` value set in ``Object.create``.

.. code-block:: text
   :caption: Example Global Ambient Sound

   rem ************ AmbientSounds ************
   rem Global ambient sound played throughout the level:
   rem [SoundObjectTemplate: S_GlobalAmbient]
   ObjectTemplate.create Sound S_GlobalAmbient
   ObjectTemplate.activeSafe Sound S_GlobalAmbient
   ObjectTemplate.modifiedByUser esj
   ObjectTemplate.lowSamples 2147483647
   ObjectTemplate.mediumSamples 2147483647
   ObjectTemplate.soundFilename "common/sound/levelambients/dalian_plant/dalian_plant_global_ambience.ogg"
   ObjectTemplate.loopCount 0
   ObjectTemplate.is3dSound 0
   ObjectTemplate.stopType 0
   ObjectTemplate.volume 0.74
   ObjectTemplate.pitch 1
   ObjectTemplate.pan 0.5
   ObjectTemplate.reverbLevel 0
   ObjectTemplate.minDistance 300000

   Sound.addTrigger S_GlobalAmbient

.. code-block:: text
   :caption: Example Positional Ambient Sound

   rem [SoundObjectTemplate: S_Carrier_Ambience_1]
   ObjectTemplate.create Sound S_Carrier_Ambience_1
   ObjectTemplate.activeSafe Sound S_Carrier_Ambience_1
   ObjectTemplate.modifiedByUser esj
   ObjectTemplate.isNotSaveable 1
   ObjectTemplate.lowSamples 2147483647
   ObjectTemplate.mediumSamples 2147483647
   ObjectTemplate.soundFilename "common/sound/levelambients/gulf_of_oman/carrier_ambient.ogg"
   ObjectTemplate.loopCount 0
   ObjectTemplate.is3dSound 0
   ObjectTemplate.stopType 0
   ObjectTemplate.volume 1
   ObjectTemplate.pitch 1
   ObjectTemplate.pan 0.5
   ObjectTemplate.reverbLevel 0
   ObjectTemplate.position 776.031/155.718/77.343
   ObjectTemplate.minDistance 50

   Sound.addTrigger S_Carrier_Ambience_1

   Object.create S_Carrier_Ambience_1
   Object.absolutePosition 776.031/155.718/77.343
   Object.rotation 0.000/0.000/0.000
   Object.layer 1

Testing Ambient Objects
-----------------------

To test your changes in-game:

#. Edit the :file:`AmbientObject.con` file within :file:`server.zip`.
#. Set the ``ObjectTemplate.chance`` to ``1`` and ``ObjectTemplate.minimumTimeBetweenTriggering`` to ``0``.
#. Open the BF2 Editor, switch to :guilabel:`LevelEditor`, and load the level via :menuselection:`File --> Load`.

Once the level has loaded:

#. Open the resources bar and expand the :guilabel:`Ambient` section.
#. Navigate to :guilabel:`AmbientTrigger`, select its sub-folder, and then select an individual effect.
#. In the level settings on the right side, locate the :guilabel:`Minimap` section and click :guilabel:`Show`.
#. Load the level in-game and test the identified ``AmbientEffects``.

.. tip::

   After selecting a new trigger, move the camera to update the position on the minimap.
