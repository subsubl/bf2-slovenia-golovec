
BF2 Coordinates
===============

Battlefield 2 uses a basic 3D coordinate system to define the position and orientation of objects in the game world.

Only objects from the :py:class:`PhysicalObject` class and its subclasses (like :py:class:`soldierObject` or :py:class:`controlPointObject`) have positions and orientations in the game world. For instance, :py:class:`bf2.PlayerManager.Player` objects do not have positions or orientations.

To get the position and orientation of a vehicle (e.g., an Abrams tank), represented by the :py:class:`vehicleObject` ``tank``:

.. code-block:: python

   position = tank.getPosition()
   rotation = tank.getRotation()

To get a player's position and orientation, represented by the :py:class:`bf2.PlayerManager.Player` object ``andreas``:

.. code-block:: python

   # Get the SoldierObject containing andreas
   andreasSoldier = andreas.getVehicle()
   position = andreasSoldier.getPosition()
   rotation = andreasSoldier.getRotation()

Position
--------

Coordinates are specified by a three-element tuple, ``(X, Y, Z)``. For example:

.. code-block:: python

   (-160.95599365234375, 162.54800415039062, -266.01699829101562)

Within :file:`.con` files these coordinates are written with slashes: ``X/Y/Z``.

These coordinates define a position along three axes:

``X``
   Indicates how far East or West an object is. Moving East/West increases/decreases this value.

``Y``
   Represents altitude. Increases with height.

``Z``
   Indicates how far North or South an object is. Moving North/South increases/decreases this value.

In all BF2 maps, the coordinate system's origin (0, 0) is at the map's center. Each unit in the system is roughly 1 meter in the game. So, the example coordinate means a point 160.96 meters east and 266.02 meters south of the map center, at an altitude of 162.55 meters. This is an absolute altitude; the altitude relative to the ground changes based on the terrain, and 'sea level' varies across maps.

The base Battlefield 2 game includes two map sizes. You can find the map size using the :py:meth:`bf2.gameLogic.getWorldSize` method, which returns a two-element tuple showing the map's East/West and North/South dimensions in meters. Most maps, except Strike at Karkand, return (2048, 2048), meaning they are 4 square kilometers (2048x2048 meters) with coordinates from -1024 to +1024 in each direction. Strike at Karkand is unique, returning (1024, 1024), which means it's 1 square kilometer with coordinates from -512 to +512.

   :py:meth:`bf2.gameLogic.getWorldSize` likely gets its information from the ``heightmapcluster.setHeightmapSize`` parameter in ``Battlefield 2/mods/bf2/Levels/<name of map>/server.zip/Heightdata.con``.

.. code-block:: python
   :caption: The distance between any two points can easily be found by using the Pythagorean Theorem

   import math

   def findDistance(point1, point2):
      '''
      Calculates the distance between two sets of coordinates using the Pythagorean Theorem.
      With standard BF2 scaling, the result is in meters.
      '''
      deltaX = math.fabs(point1[0] - point2[0])
      deltaY = math.fabs(point1[1] - point2[1])
      deltaZ = math.fabs(point1[2] - point2[2])

      distance = math.sqrt(deltaX * deltaX + deltaY * deltaY + deltaZ * deltaZ)

      return distance

Rotation
--------

.. code-block:: python
   :caption: Rotation (attitude) is defined by another three-element tuple: (A, P, R)

   (166.29025268554687, 0.0, 0.0)

Within :file:`.con` files, these angles are written with slashes: ``A/P/R``.

``A``
   ("azimuth" or "yaw") shows rotation from due north, measured in degrees. Positive values are clockwise, negative are counter-clockwise. This is how much your view rotates around a vertical axis.

   :0: Due North
   :90: Due East
   :180: Due South
   :270: Due West

``P``
   ("pitch") indicates how much you are tilting up or down from horizontal, measured in degrees. This is the tilt along the axis passing through your viewpoint from left to right.

   :-90: Looking straight up
   :-45: Tilting up halfway between horizonal and vertical
   :0: Horizontal
   :45: Tilting down halfway between horizontal and vertical
   :90: Looking straight down

``R``
   ("roll") shows how much the viewpoint has rotated around its front-to-back axis, measured in degrees:

   :-45: Viewpoint is rolled clockwise by 45 degrees
   :0: No roll
   :45: Viewpoint is rolled counter-clockwise by 45 degrees

.. note::

   Pitch and roll rotations apply to aircraft and cameras in BF2, but not to ground players or vehicles. Ground units always show P and R as 0, even if their actual orientation suggests otherwise (e.g., a soldier looking straight up still has a P value of 0).
