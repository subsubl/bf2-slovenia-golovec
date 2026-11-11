
Simplified Overgrowth Field Placement
=====================================

:Original Author: [R-DEV] Outlawz7 (Retired)

.. important::

   The original version contains images that are no longer available.

This tutorial outlines a simplified process for overgrowth field placement, based on the established workflow described in `Rhino's Overgrowth Tutorial <https://www.realitymod.com/forum/f189-modding-tutorials/66161-map-tutorial-overgrowth-field-placement.html>`_.

Prerequisites
-------------

* :program:`Battlefield 2 Editor v1.3`
* :program:`Notepad++`
* An advanced hex or text editor

  e.g., Visual Studio Code with the `Hex Editor Extension <https://marketplace.visualstudio.com/items?itemName=ms-vscode.hexeditor>`_.

Preparation
-----------

Create backups of the following files:

* The :file:`Overgrowth/` folder.
* :file:`Staticobjects.con`.
* Any GPO and :file:`Layer.con` files in the :file:`Editor/` folder.

Rename GPO and :file:`Layer.con` files (e.g., append a prefix like :file:`asdfLayer.con`) to disable them without modifying their content.

Step 1: Placing Overgrowth
--------------------------

#. Load the map in the editor and switch to the terrain editor.
#. Use the Overgrowth tool to create one or more overgrowth materials, selecting the field geometries from :file:`vegetation/PR/fields/`.
#. In the resource tab, navigate to the :guilabel:`General` settings and configure the following:

   .. describe:: Draw Distance

      The distance at which overgrowth is rendered. Set this to a value such as ``50`` or ``150``.

#. Configure the density and radius settings:

   .. describe:: Density

      The density of the overgrowth. Set this value between ``100`` and ``300``.

   .. describe:: MinRadiusToSame

      The minimum radius to the same object. Set this between ``0.2`` and ``0.4``. Configure the radius first, then increase the density.

Step 2: Converting Overgrowth
-----------------------------

#. Switch to the level editor and navigate to the :guilabel:`Layers` tab.
#. :kbd:`Right-click` :guilabel:`Layer 1`, select :guilabel:`Select all in layer`, and press :kbd:`Delete`. This clears static objects from the layer.
#. Place a small static object in the map and apply Low-quality lightmapping to convert the overgrowth to static objects.
#. Set the Overgrowth density to ``0`` to minimize performance impact.
#. Delete the lightmapped object.
#. Select the overgrowth fields. Use the :guilabel:`Select all of the same type` option to ensure all fields are selected.
#. In the TweakBar, configure the following:

   .. describe:: isSaveable

      A setting that determines if the layer is saveable. Set this to ``1``.

#. Save the map. Ignore warnings regarding lightmap/object mismatches.

Step 3: Finalizing Overgrowth
-----------------------------

#. Verify the :file:`Staticobjects.con` file. It should contain only the run commands and object positions for the fields.
#. Close the editor.
#. Optional: To treat fields as normal objects (avoiding light/dark spots), use a hex editor to open :file:`Staticobjects.con` and replace the following:

   .. describe:: Object.isOvergrowth

      A technical parameter within :file:`Staticobjects.con`. Replace ``Object.isOvergrowth 1`` with an empty string.

#. To integrate the fields into the main :file:`Staticobjects.con`, copy the field-related lines and paste them into the original, backed-up :file:`Staticobjects.con` file.
#. Rename the backed-up files to their original names and delete the generated overgrowth folder.
#. Reload the map in the editor to continue working with the finalized overgrowth fields.
