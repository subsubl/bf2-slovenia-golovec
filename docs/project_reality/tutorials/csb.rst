
Close Support Bridges (CSB) Placement
=====================================

:Original Author: [R-DEV] Rhino (Retired)

.. important::

   The original version has images that are not available anymore.

This tutorial provides instructions for the correct placement of Close Support Bridges (CSB) in maps to ensure professional and functional results.

This tutorial focuses on the British BR90 series of CSBs, but the steps apply to other types. Review the following Highlight Post regarding these assets before proceeding: `Close Support Bridges (CSB) <https://www.realitymod.com/forum/f196-pr-highlights/82503-close-support-bridges-csb.html>`_.

CSB Section Types
-----------------

The BR90 CSB system consists of eight sections located in :file:`/objects/common/deployable_csb`. The sections are categorized into three main types:

* **No. 10 Section**: 22 m long.
* **No. 10 with Trestle Attachment**: 18 m long.
* **No. 11 Section**: 15 m long.

Each type includes variations: the bridge section alone, a section with a Single Dirt Support (SDS) on one end, and a section with a Double Dirt Support (DDS) on both ends.

Real-Life Usage
---------------

Implementing real-life CSB usage increases in-game realism. The Royal Engineers define CSBs as mechanically launched bridges for gap crossing in combat zones, providing crew protection through armor. For more information, visit the `British Army Website <http://www.army.mod.uk/royalengineers/equipment/702.aspx>`_.

In reality, specialized vehicles such as an Armoured Vehicle Launched Bridge (AVLB) like the TITAN, or a Tank Bridge Transporter (TBT), deploy CSBs. Project Reality uses logistics trucks for deployment.

When placing bridges, consider bank height differences and use appropriate combination bridging techniques. Trestle rotation is generally flat with the surface, but a slight rotation of the trestle top is permissible as long as it remains perpendicular to the ground.

Setting Up the Editor
---------------------

To ensure CSBs and deployable objects render correctly and do not appear black, follow these setup steps:

#. Download the modified shader: `Modified_RaShaderBM_for_tis_28-11-10.rar <http://realitymodfiles.com/rhino/editor/Modified_RaShaderBM_for_tis_28-11-10.rar>`_.
#. Navigate to :file:`<BF2_INSTALL_DIR>/bf2editor/Shaders` and create a backup of the existing :file:`RaShaderBM.fx`.
#. Extract the modified :file:`RaShaderBM.fx` from the downloaded file into the :file:`<BF2_INSTALL_DIR>/bf2editor/Shaders` directory.
#. Navigate to :file:`/Documents/Battlefield 2/cache` and delete all folders within the directory.
#. Restart the editor.

Placing CSBs
------------

CSBs are placed as static objects and saved within the map's :file:`Staticobjects.con` file.

.. note::

   Before deploying bridges, render both Overgrowth and Undergrowth objects to avoid placing bridges inside vegetation.

Single Section Bridging
^^^^^^^^^^^^^^^^^^^^^^^

#. Use the :guilabel:`Measure` tool to determine the gap width.
#. Select the appropriate CSB section based on the measurement. For a standard gap, the No. 10 DDS section provides a level foundation.
#. Drag and drop the section into the map.
#. **Testing**: To test bridge functionality in the editor:

   * Place a vehicle near the CSB.
   * In the command bar, type :code:`camera.OnVehicleMode` and press :kbd:`Enter`.
   * Use :kbd:`WASD` to control the vehicle and test the bridge.
   * To exit, select :menuselection:`Camera --> Normal Mode`.

Combination Bridging
^^^^^^^^^^^^^^^^^^^^

When a gap exceeds the length of a single CSB section, join multiple sections. This can be done by overlapping sections or using the trestle attachment. Ensure that the dirt supports are placed correctly to provide a level bridge surface.

Trestle Combination Bridging
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use trestle attachments to support bridges over wide gaps or rivers. Position the trestle so it sits flat on the terrain or water bed. Ensure the trestle remains perpendicular to the ground.

Overbridging
^^^^^^^^^^^^

Overbridging involves placing a CSB over an existing bridge. This is useful for reinforced crossing or bridging holes in destroyed bridge sections.

#. In the editor, view the bridge in its wrecked state by selecting the destroyable section and changing the :guilabel:`SubGeometry` value from ``0`` to ``1`` in the Geometry Component of the Tweaker Bar. (This is for visualization only and does not affect in-game behavior).
#. Place the CSB section on top of the bridge.
#. Avoid using dirt supports when overbridging to prevent clipping through the original bridge structure.

Design Considerations
---------------------

* **Networkable Objects**: Destructible objects contribute to the networkable object limit. Excessive use of CSBs can cause server instability. To preserve capacity for other assets, aim for fewer than 300 destructible objects per map. Verify the total count using the :guilabel:`Level Info` tool.
* **Spacing**: Unless a specific location requires it, place CSB locations at least 100 m apart to provide flexibility and prevent deployment errors.
* **Z-Fighting**: Place dirt supports slightly above the terrain to prevent z-fighting.
* **Floating Sections**: Bridge sections may appear to float if supporting sections are destroyed or deployed incorrectly; however, this is an acceptable trade-off for the gameplay utility of the CSB system.
* **Anchors**: Use bridge section anchors to assist with rotation and positioning. Hold :kbd:`Shift` while in rotation mode to move the rotation gizmo to the anchor position.
