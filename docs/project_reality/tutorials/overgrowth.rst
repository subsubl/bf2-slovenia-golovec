
Advanced Overgrowth Placement
=============================

:Original Author: Rabbit

This tutorial demonstrates advanced overgrowth (OG) placement in woodland settings, focusing on realism, gameplay, and optimization. The effectiveness of this technique depends on map size and location. This document does not provide a detailed explanation of elevation or overgrowth types.

Traditional techniques involve creating one or two settings and painting them across the map. This can be accomplished using high-density settings in small patches (e.g., ``Kham``) or large areas with low to medium density (e.g., ``Hades Peak``). This tutorial utilizes a combination of both methods.

Compare ``Fools Road`` and ``Nuijamaa`` to observe the impact of overgrowth counts. As of PR 1.3, ``Fools Road`` contains 23,194 OG objects, while ``Nuijamaa`` contains 10,059; however, ``Nuijamaa`` maintains a more forested appearance.

.. figure:: http://i.imgur.com/587Fp49.jpg
   :align: center

   Fools Road.

.. figure:: http://i.imgur.com/1D0hfB5.png
   :align: center

   Nuijamaa.

Nuijamaa maintains a more forested appearance despite having less than half the OG objects. This is partly due to the use of fir clusters on Nuijamaa, which may leave more unused space.

.. image:: http://i.imgur.com/587Fp49.jpg
   :align: center

In the ``Fools Road`` image, observe how woods terminate at fields and how unimproved roads separate forest "islands." These features have both natural and gameplay implications.

.. image:: http://i.imgur.com/U3hMF0X.jpg
   :align: center

Grasslands surrounding forest islands often contain growing shrubs because sunlight reaches the edges. As the sun moves from east to west, areas under the trees at the forest edge are exposed. Deciduous trees branch out to cover the forest interior, blocking sunlight and reducing shrub growth. This creates pockets of safety for infantry on the forest edge, allowing for greater freedom of maneuver. Because shrubs are concentrated on the edges, it prevents enemies from easily hiding in them, providing a balance for infantry movement.

.. image:: http://i.imgur.com/Nk5Sn4j.jpg
   :align: center

Small roads cutting through woods also affect this. An unimproved road through a woodland corridor allows some sunlight to reach the edges, resulting in lower shrub density than a field adjacent to woods. Utilizing low shrubs instead of large ones can create a clear path for infantry. Tree height, foliage spread, and the distance between islands also influence shrub growth.

.. image:: http://i.imgur.com/2gKUaDo.png
   :align: center

In-Game Creation
----------------

Recreating these settings is straightforward but requires more time than simpler methods.

.. describe:: Type 1: Woods

   A high-density setting used for primary woodland areas.

   .. code-block:: text

      Overgrowth.addMaterial woods 1
      Overgrowth.setActiveMaterial woods
      Overgrowth.addType fir1
      Overgrowth.setActiveType fir1
      OvergrowthType.geometry fir_mixed01
      OvergrowthType.density 4
      OvergrowthType.normalScale 0.05
      OvergrowthType.rotationScale 0
      OvergrowthType.minRadiusToSame 0.15
      OvergrowthType.minRadiusToOthers 0.35
      Overgrowth.addType fir2
      Overgrowth.setActiveType fir2
      OvergrowthType.geometry fir_mixed02
      OvergrowthType.density 4.5
      OvergrowthType.normalScale 0.05
      OvergrowthType.rotationScale 0
      OvergrowthType.minRadiusToSame 0.2
      OvergrowthType.minRadiusToOthers 0.3
      Overgrowth.addType shrub
      Overgrowth.setActiveType shrub
      OvergrowthType.geometry deciduous_bush_1
      OvergrowthType.density 1
      OvergrowthType.normalScale 1
      OvergrowthType.rotationScale 0
      OvergrowthType.minRadiusToSame 1
      OvergrowthType.minRadiusToOthers 0
      Overgrowth.addType birch1
      Overgrowth.setActiveType birch1
      OvergrowthType.geometry birch_green_1
      OvergrowthType.density 1.5
      OvergrowthType.normalScale 0.05
      OvergrowthType.rotationScale 0
      OvergrowthType.minRadiusToSame 0.35
      OvergrowthType.minRadiusToOthers 0.35
      Overgrowth.addType log
      Overgrowth.setActiveType log
      OvergrowthType.geometry nc_deadlog01
      OvergrowthType.density 1
      OvergrowthType.normalScale 1
      OvergrowthType.rotationScale 0
      OvergrowthType.minRadiusToSame 0.4
      OvergrowthType.minRadiusToOthers 0

.. describe:: Type 2: Woods-edge

   A medium-density setting used for transition zones between forest and open areas.

   .. code-block:: text

      Overgrowth.addMaterial woodsedge 2
      Overgrowth.setActiveMaterial woodsedge
      Overgrowth.addType fir2
      Overgrowth.setActiveType fir2
      OvergrowthType.geometry fir_mixed02
      OvergrowthType.density 6
      OvergrowthType.normalScale 0.05
      OvergrowthType.rotationScale 0
      OvergrowthType.minRadiusToSame 0.28
      OvergrowthType.minRadiusToOthers 0.3
      Overgrowth.addType birch
      Overgrowth.setActiveType birch
      OvergrowthType.geometry birch_green_2
      OvergrowthType.density 5
      OvergrowthType.normalScale 0.05
      OvergrowthType.rotationScale 0
      OvergrowthType.minRadiusToSame 0.35
      OvergrowthType.minRadiusToOthers 0.35
      Overgrowth.addType oak
      Overgrowth.setActiveType oak
      OvergrowthType.geometry nc_oak02
      OvergrowthType.density 3
      OvergrowthType.normalScale 0.05
      OvergrowthType.rotationScale 0
      OvergrowthType.minRadiusToSame 0.35
      OvergrowthType.minRadiusToOthers 0.35
      Overgrowth.addType bigshrub
      Overgrowth.setActiveType bigshrub
      OvergrowthType.geometry shrub_01
      OvergrowthType.density 8
      OvergrowthType.normalScale 1
      OvergrowthType.rotationScale 0
      OvergrowthType.minRadiusToSame 0
      OvergrowthType.minRadiusToOthers 0

.. describe:: Type 3: Low Play

   A low-density setting used for areas with infrequent player travel or at map edges.

   .. code-block:: text

      Overgrowth.addMaterial lowplay 3
      Overgrowth.setActiveMaterial lowplay
      Overgrowth.addType fir1
      Overgrowth.setActiveType fir1
      OvergrowthType.geometry fir_mixed01
      OvergrowthType.density 1.8
      OvergrowthType.normalScale 0.05
      OvergrowthType.rotationScale 0
      OvergrowthType.minRadiusToSame 0.15
      OvergrowthType.minRadiusToOthers 0.35
      Overgrowth.addType fir2
      Overgrowth.setActiveType fir2
      OvergrowthType.geometry fir_mixed02
      OvergrowthType.density 1.6
      OvergrowthType.normalScale 0.05
      OvergrowthType.rotationScale 0
      OvergrowthType.minRadiusToSame 0.35
      OvergrowthType.minRadiusToOthers 0.35
      Overgrowth.addType bush
      Overgrowth.setActiveType bush
      OvergrowthType.geometry deciduous_bush_1
      OvergrowthType.density 0.7
      OvergrowthType.normalScale 1
      OvergrowthType.rotationScale 0
      OvergrowthType.minRadiusToSame 0
      OvergrowthType.minRadiusToOthers 0

The following image color-codes these three types: ``Dark blue (woods)``, ``light blue (woods-edge)``, and ``green (low play)``.

.. image:: http://i.imgur.com/r3iwwji.png
   :align: center

The image illustrates the colors alongside wood islands and the map edge. Start by painting large wood islands based on your reference. Next, use the ``woodsedge`` layer with a mix of deciduous trees and shrubs along the edges. Finally, replace ``woods`` with ``lowplay`` in areas where ``woodsedge`` is dense, such as near the center of the image. This works because the high density of ``woodsedge`` requires fewer OG pieces between lines. Use ``lowplay`` along map edges or in areas where player travel is infrequent. Using a thinned-out overgrowth layer at map edges helps prevent players from easily using them as safe travel points.

.. note::

   Using this technique with fir clusters reduces overgrowth counts while maintaining the appearance of a dense forest. This approach helps maintain high FPS for users with lower-end hardware. This is only one of many possible techniques.
