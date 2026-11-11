
Map Asset Sizing and Dimension Guide
====================================

:Original Author: Rhino

This guide provides standard dimensions for static objects and map geometry. Following these guidelines ensures that players can move through doorways, climb stairs, and shoot over walls as expected.

.. note::

   The minimum and maximum values listed are absolute limits. For the best results, aim for the recommended values whenever possible.

Player Movement
---------------

Use these values to define gaps and openings that players need to move through.

.. describe:: Standing Gap

   The minimum height for a player to pass through while standing.

   :Min Height: 1.7m

.. describe:: Crouching Gap

   The minimum height for a player to pass through while crouching. The visual height should be slightly smaller than the collision height to prevent the player's head from clipping through the object in 3rd-person view.

   :Min Collision Height (col2): 1.4m
   :Min Visual Height (3rd-person): 1.3m

.. describe:: Prone Gap

   The minimum height for a player to crawl through.

   :Min Height: 0.52m

.. describe:: Width

   The minimum width for any player movement gap.

   :Min Width: 0.5m

Structures
----------

.. describe:: Doorways

   Required dimensions for the breachable door system.

   :Recommended Height: 2.0m
   :Recommended Width: 1.0m
   :Recommended Frame Thickness: 0.04m

.. describe:: Gateways

   Required dimensions for the 3-meter wide gates.

   :Min Height: 2.5m
   :Min Width: 3.05m
   :Recommended Height: 3.0m or more
   :Recommended Width: 3.06m

Player Traversal
----------------

.. describe:: Jumping

   The maximum height a player can jump over.

   :Standing Jump: 1.37m
   :Walking Jump: 1.45m
   :Sprinting Jump: 1.62m

.. describe:: Climbing and Stairs

   The maximum angle a player can climb depends on the collision material used.

   .. list-table::
      :header-rows: 1

      * - Material Type
        - Recommended Max Angle
        - Absolute Max Angle (with difficulty)
      * - Normal Material
        - <40°
        - ~45°
      * - Stairs Material
        - <50°
        - ~55°
      * - Steep Stairs Material
        - <60°
        - ~65°

Combat Positions
----------------

Cover Heights
^^^^^^^^^^^^^

The height required to provide cover for a player.

.. describe:: Standing Cover

   :Min Height: 1.65m
   :Recommended Height: 1.7m or more

.. describe:: Crouched Cover

   :Min Height: 1.15m
   :Recommended Height: 1.3m or more (at 1.3m, the top of the helmet is visible when moving)

.. describe:: Prone Cover

   :Min Height: 0.55m
   :Recommended Height: 0.6m or more

Firing Position Heights
^^^^^^^^^^^^^^^^^^^^^^^

The maximum height of an object a player can shoot over from a specific stance.

.. describe:: Standing Firing Position

   :Max Height: 1.47m
   :Recommended Height: 1.32m

.. describe:: Crouched Firing Position

   :Max Height: 0.95m
   :Recommended Height: 0.85m

.. describe:: Prone Firing Position

   :Max Height: 0.37m
   :Recommended Height: 0.3m to 0.35m

Vehicles
--------

.. describe:: Vehicle Gaps

   The minimum width for vehicles to pass through.

   :ATV Gap Min Width: 1.2m
