
Creating Undergrowth and Overgrowth Environments
================================================

:Original Author: Amok@ndy

.. important::

   The original version has images that are not available anymore.

This tutorial explains how to create an Undergrowth and Overgrowth environment. This method is applicable to various map sizes, including 4 km maps.

Requirements
------------

* :file:`bf2_tpaint` or a map with colored layers 1-3.

Step 1: Configure Undergrowth
-----------------------------

#. Open the map in the editor.
#. Navigate to the terrain editor and select the :guilabel:`Undergrowth Tool`.
#. Create three materials using the first three color-coded buttons (:guilabel:`[1]`, :guilabel:`[2]`, and :guilabel:`[3]`).

Step 2: Import Detail Layers
----------------------------

#. Select the :guilabel:`Import DetailLayers` button in the toolbar.
#. Enable Undergrowth mode by navigating to :menuselection:`Render --> Undergrowth Mode` to verify the configuration.

Step 3: Configure Overgrowth
----------------------------

#. Select the :guilabel:`Undergrowth Tool`.
#. Create three materials using the same color-coded buttons (:guilabel:`[1]`, :guilabel:`[2]`, and :guilabel:`[3]`) used for the Undergrowth configuration.
#. Assign the desired trees and bushes to the materials and save the map.

Step 4: Synchronize Data
------------------------

#. Keep the editor open throughout this process.
#. Navigate to the map's folder in your file explorer.
#. Copy the :file:`Undergrowth.raw` file.
#. Navigate to the Overgrowth folder, delete the existing :file:`Overgrowth.raw` file, and paste the copied :file:`Undergrowth.raw` file.
#. Rename the pasted :file:`Undergrowth.raw` file to :file:`overgrowth.raw`.

Step 5: Finalize
----------------

#. Return to the editor and reload the map.
#. The Undergrowth and Overgrowth environments are now synchronized.
