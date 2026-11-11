
Sorting Statics for Lightmapping
================================

To begin, unhide all :guilabel:`LOD0` static meshes. The most efficient method is to use the **Unhide by Name** feature and search for :guilabel:`*=0` to select all required :guilabel:`LOD0` meshes.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000143.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000144.jpg
   :align: center

Next, navigate to :menuselection:`BF2 --> Bf2 Lightmapping` and click :guilabel:`Save/Update File` in the :guilabel:`Lightmap Size Control` section. Save the :file:`.txt` file with a descriptive name, such as :file:`YourMap_LightmapSizes.txt`.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000145.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000146.jpg
   :align: center

Open the newly created file. It lists all lightmappable statics and their LODs. Currently, each LOD has an :guilabel:`undefined` lightmap size that must be defined.

.. code-block:: text

   hotel  undefined  undefined  undefined  undefined
   house_high_02_v2  undefined  undefined  undefined  undefined
   house_high_03  undefined  undefined  undefined  undefined
   house_high_04  undefined  undefined  undefined  undefined
   house_high_05  undefined  undefined  undefined  undefined
   house_high_06  undefined  undefined  undefined  undefined
   house_medium_02  undefined  undefined  undefined  undefined
   house_medium_05  undefined  undefined  undefined  undefined
   citybuilding_2a_part1  undefined  undefined  undefined  undefined
   citybuilding_2a_part2  undefined  undefined  undefined  undefined
   citybuilding_3a  undefined  undefined  undefined  undefined
   housingblock_1_groundfloor  undefined  undefined  undefined  undefined
   housingblock_1_midfloor_v2  undefined  undefined  undefined  undefined
   housingblock_1_midfloor_v1  undefined  undefined  undefined  undefined
   housingblock_1_topfloor  undefined
   house_double_02  undefined  undefined  undefined  undefined
   house_double_04  undefined  undefined  undefined  undefined
   citybuilding_4a  undefined  undefined  undefined  undefined
   dock_straight_30m  undefined  undefined
   dock_bend_122degs  undefined  undefined
   house_detached_02  undefined  undefined  undefined  undefined
   house_detached_03  undefined  undefined  undefined  undefined
   house_detached_01  undefined  undefined  undefined
   house_low_01  undefined  undefined  undefined  undefined
   house_low_03  undefined  undefined  undefined
   house_low_02_v2  undefined  undefined  undefined
   mi_hangar_mec  undefined  undefined  undefined
   xp1_airtower  undefined  undefined  undefined  undefined
   fishingboat  undefined  undefined  undefined  undefined
   boxesonpallet_01  undefined  undefined  undefined
   woodencrate_3m  undefined  undefined  undefined
   marketstand_1  undefined  undefined
   parkbench  undefined  undefined  undefined
   plant_box  undefined
   phonebooth  undefined  undefined  undefined
   rockpile_1  undefined  undefined  undefined
   rockpile_large  undefined  undefined  undefined
   rockpile_medium  undefined  undefined  undefined
   rockpile_medium_02  undefined  undefined  undefined
   container_cl_blue  undefined  undefined
   container_cl_green_trash  undefined  undefined  undefined
   container_cl_red  undefined  undefined
   container_cl_yellow  undefined  undefined
   container_op_yellow_cluster  undefined  undefined
   basket_hoops  undefined  undefined
   smallboat1  undefined  undefined  undefined
   smallboat2  undefined  undefined  undefined
   smallboat3  undefined  undefined  undefined
   lighthouse  undefined  undefined  undefined  undefined
   tyre_stack_v1  undefined  undefined  undefined
   shack_v4  undefined  undefined  undefined
   boatwreck_small  undefined  undefined  undefined  undefined
   pier  undefined  undefined  undefined
   car1  undefined  undefined  undefined  undefined
   water_cart_v1  undefined  undefined  undefined
   palletstack  undefined  undefined  undefined
   bus_stop  undefined  undefined  undefined
   cafechair  undefined  undefined  undefined
   trash_dumpster  undefined  undefined
   tvset  undefined  undefined  undefined
   lamppost_highway_01  undefined  undefined  undefined
   shack_v2  undefined  undefined  undefined
   construct_metal_plate  undefined  undefined
   shack_v3  undefined  undefined  undefined
   lamp_post  undefined  undefined  undefined
   shack_v5  undefined  undefined  undefined
   spawn_shack  undefined  undefined  undefined
   shack_v1  undefined  undefined  undefined
   water_tower  undefined  undefined  undefined
   gb_carrier_invincible_back  undefined  undefined  undefined  undefined
   gb_carrier_invincible_bridge  undefined  undefined  undefined  undefined
   gb_carrier_invincible_front  undefined  undefined  undefined  undefined
   gb_carrier_invincible_mid  undefined  undefined  undefined  undefined
   gb_carrier_invincible_skijump  undefined  undefined  undefined  undefined
   gb_carrier_invincible_interior_pt2  undefined  undefined  undefined  undefined
   gb_carrier_invincible_interior_pt1  undefined  undefined  undefined  undefined
   air_repairstation_no_supply  undefined  undefined  undefined
   mi_antenna  undefined  undefined  undefined
   mi_plane_stair  undefined  undefined  undefined
   mi_barrack_mech  undefined  undefined  undefined  undefined
   bunker  undefined  undefined  undefined

.. tip::

   You can merge this file with the existing :file:`Master LightmapSizes` file to leverage pre-defined sizes.

   #. Download the master list: :download:`master_size.txt <https://files.realitymod.com/lightmapping/master_size.txt>`
   #. Open it with a text editor, then append its contents to the end of your :file:`YourMap_LightmapSizes.txt` file and save.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000155.jpg
   :align: center

To sort objects alphabetically while keeping their LODs grouped, use a spreadsheet application like Google Sheets.

#. Create a new spreadsheet in Google Drive.
#. Import the :file:`.txt` file via :menuselection:`File --> Import`.
#. Select :guilabel:`Replace spreadsheet` and set the separator character to a space (" ").

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000147.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000148.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000149.jpg
   :align: center

With :guilabel:`Column A` selected, navigate to :menuselection:`Data --> Sort --> Sheet by column A --> A > Z` to sort all rows alphabetically.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000150.jpg
   :align: center

Search the file for :guilabel:`undefined` to see if settings are already defined in the master list. For example, :guilabel:`air_repairstation_no_supply` may already be defined in the preceding row.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000160.jpg
   :align: center

When an object is not already defined, copy it into the master :file:`.txt` file.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000161.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000162.jpg
   :align: center

Update the :guilabel:`undefined` LOD lightmap sizes by browsing the object's lightmap samples with **BFMeshView**. The :file:`.samples` file corresponds to LOD0, :file:`.samp_01` to LOD1, and so on.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000166.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000164.jpg
   :align: center

The width and height of the lightmap are displayed in the top-left corner of the viewer.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000165.jpg
   :align: center

Many lightmap samples use a higher resolution than necessary. Reducing resolution, especially for LODs, can optimize performance. For example, the default :guilabel:`lod1` lightmap for a bunker might be 128x128, which can be reduced to 64x64, with :guilabel:`lod2` set to 32x32.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000167.jpg
   :align: center

If an object requires non-square lightmaps, define them using an asterisk (e.g., :file:`256*64`). Only a few objects with custom lightmap UVs, such as the `Wooden Fence Series <https://www.realitymod.com/forum/f196-pr-highlights/93602-new-wooden-fence-statics.html>`_, are configured this way.

.. important::

   The width and height of each lightmap must be a power of two (e.g., 8, 16, 32, 64, 128, 256, 512, 1024, or 2048).

If an object lacks any samples, determine the appropriate lightmap size through trial and error.

Once you have defined the lightmap sizes for all LODs in the :file:`Master_LightmapSizes.txt` file, return to 3ds Max. Navigate to :menuselection:`BF2 --> BF2 Lightmapping` and load the updated :file:`Master_LightmapSizes.txt`. Click :guilabel:`Apply Lightmap Settings` to apply these sizes to all LODs of your statics.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000168.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000169.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000170.jpg
   :align: center
