
Avoiding the Vehicle Engine Sound Bug
=====================================

:Original Author: [R-DEV] Jaymz (Retired)

Insufficient view distance on a map can cause a sound bug where players hear vehicle engine sounds for vehicles that are not visible.

Required View Distances
-----------------------

To prevent this bug, ensure the map's view distance meets the minimum requirements for the vehicle types included:

.. list-table:: Minimum View Distances
   :header-rows: 1

   * - Vehicle Type
     - Minimum View Distance
   * - Jets
     - 1 km
   * - Helicopters
     - 800 m
   * - Tanks and large tracked vehicles
     - 600 m
   * - Other vehicles
     - 300 m

Design Considerations
---------------------

New Maps
^^^^^^^^

When creating a new map, configure the view distance based on the planned vehicle assets. For example, if the map includes helicopters, the view distance must be at least 800m.

Existing Maps
^^^^^^^^^^^^^

If an existing map experiences this bug, remove the problematic vehicle assets or increase the map's view distance. Increasing the view distance may not be feasible depending on the original map design.
