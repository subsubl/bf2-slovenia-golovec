
Parachute Spawns
================

Most parachute spawn functionality is managed by Python. Planes travel at a speed of 50-60 meters per second (180-216 km/h).

Spawning Requirements
---------------------

To ensure correct functionality, the :program:`ObjectSpawner` must meet the following criteria:

#. The object name must include ``paradrop``.
#. A team must be assigned to the spawner to prevent incorrect marker generation.
#. The ``TimeToLive`` value must be set to 0.
#. A ``Distance`` value must be specified.

.. note::

   The spawner should be linked to the main base. Ensure the flag team matches the template team.

Configuration Parameters
-------------------------

The following parameters are critical for configuring parachute spawns:

.. describe:: ObjectSpawner

   A technical object used to define spawn points. The rotation of this object determines the direction of movement for spawned entities.

.. describe:: TimeToLive

   Sets the lifespan of the spawned object. For parachute spawners, this value must be 0.

.. describe:: Distance

   Defines the distance the plane travels before it disappears.

.. describe:: team

   Assigns the spawner to a specific team.

Examples
--------

.. code-block:: text
   :caption: Example 1: Spawner that spawns two planes with a 10-second delay, traveling 2 km.

   ObjectTemplate.create ObjectSpawner bullseye_blue_paradrop_02
   ObjectTemplate.activeSafe ObjectSpawner bullseye_blue_paradrop_02
   ObjectTemplate.modifiedByUser "Wouter"
   ObjectTemplate.isNotSaveable 1
   ObjectTemplate.hasMobilePhysics 0
   ObjectTemplate.setObjectTemplate 2 paradrop
   ObjectTemplate.minSpawnDelay 10
   ObjectTemplate.maxSpawnDelay 10
   ObjectTemplate.TimeToLive 0
   ObjectTemplate.Distance 2000
   ObjectTemplate.teamOnVehicle 1
   ObjectTemplate.maxNrOfObjectSpawned 2
   ObjectTemplate.team 2

.. code-block:: text
   :caption: Example 2: Spawner that spawns a single plane traveling 1 km.

   ObjectTemplate.create ObjectSpawner bullseye_blue_paradrop
   ObjectTemplate.activeSafe ObjectSpawner bullseye_blue_paradrop
   ObjectTemplate.modifiedByUser "Wouter"
   ObjectTemplate.isNotSaveable 1
   ObjectTemplate.hasMobilePhysics 0
   ObjectTemplate.setObjectTemplate 2 paradrop
   ObjectTemplate.minSpawnDelay 99999
   ObjectTemplate.maxSpawnDelay 99999
   ObjectTemplate.TimeToLive 0
   ObjectTemplate.Distance 1000
   ObjectTemplate.teamOnVehicle 1
   ObjectTemplate.team 2

Implementation Considerations
------------------------------

.. warning::

   Improper configuration may result in unexpected behavior or player issues.

#. **Map Boundaries:** Ensure the ``Distance`` does not extend beyond the map boundaries. If the path exceeds the map limits, markers may incorrectly wrap around and appear on the opposite side of the map.
#. **Spawn Height:** Position the spawner at a sufficient height to prevent players from taking damage when deploying their parachutes. The spawner must not be placed on the ground.
#. **Rotation:** Apply only yaw (the X-axis value) to the ``ObjectSpawner``.
#. **Proximity to Spawn Points:** Avoid placing the plane's starting point near existing spawn points. Proximity to other spawn points may cause a green parachute icon to appear, incorrectly indicating a parachute spawn point.
