
Polycount and LOD Guidelines
============================

:Original Author: [R-DEV] eggman (Retired)

.. important::

   The original version has images that are not available anymore.

This document outlines polycount and Level of Detail (LOD) guidelines based on established standards for Battlefield 2 modding.

.. important::

   Adherence to polycount guidelines is important, but correctly implemented LOD meshes are more critical for game performance. Exceeding polycount limits by 15% has less impact on performance than missing appropriate LODs.

Weapon Models
-------------

Requirements
^^^^^^^^^^^^

Beyond the first-person view (1pv) model, the following meshes are required:

- Third-person view (3pv) mesh.
- Ironsight mesh.
- LOD1 mesh (displayed at 50-100 meters).

Polycount Guidelines
^^^^^^^^^^^^^^^^^^^^

- **Ironsight Mesh**: 1000-1100 polygons.
- **1pv Mesh (LOD0)**:

   - Assault/MG: 3000-3500 polygons.
   - Pistols: 1500-2000 polygons.

- **3pv Mesh (LOD0)**:

   - Assault/MG: 1000-1300 polygons.
   - Pistols: 700-900 polygons.

- **3pv Mesh (LOD1)**:

   - Assault/MG: 200-300 polygons.
   - Pistols: 150-200 polygons.

Vehicle Models
--------------

Requirements
^^^^^^^^^^^^

Vehicle models require a comprehensive set of meshes to ensure performance and collision accuracy:

- 1st-person mesh (for all vehicle types).
- LOD meshes (LOD0, LOD1, LOD2).
- Wreck meshes (LOD0, LOD1, LOD2).
- Collision meshes (decal, physics, and soldier collision).
