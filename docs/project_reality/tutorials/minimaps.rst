How To Make The "Perfect" Minimap
=================================

This tutorial will guide you through creating an ideal minimap for your map, ensuring all objects, trees, and other details are accurately displayed.

Requirements
------------

Tools
^^^^^

* :program:`BF2 Editor`: :download:`http://files.ancientdev.com/prbf2/PREditor.zip`
* :program:`Photoshop`: :download:`https://www.adobe.com/products/photoshop.html`
* :program:`NVIDIA DDS Plugins`: :download:`http://developer.nvidia.com/object/photoshop_dds_plugins.html`
* RAM: Larger maps will require more RAM.

Materials
^^^^^^^^^

* Your map, including editor colormap or detailmap files.

  For optimal results, the map should be finalized.

* You must have completed `Setting Up The BF2 Editor for PR Mapping/Modding <https://www.realitymod.com/forum/f189-modding-tutorials/14468-setting-up-bf2-editor-pr-mapping-modding.html>`_

Getting Started
---------------

:download:`Download these files <https://files.realitymod.com/prbf2/perfectminimapfiles.zip>`. After downloading, you will need to install them in the correct locations. The :file:`.zip` file contains two folders: ``BF2`` (for files used by the editor) and ``Photoshop`` (for files used by Photoshop).

Let's begin by installing the Photoshop files.

#. Open the Photoshop folder within the :file:`.zip` file. You will find two files: :file:`MiniMap 1024x2.atn` and :file:`MiniMap 1024x2.atn`.
#. Extract these files to :file:`C:\\Program Files\\Adobe\\Adobe Photoshop CS3\\Presets\\Actions`.

   Please note that this path may vary if Photoshop is installed in a different location or if you are using a different version. Compatibility with older versions is not guaranteed, but it should generally work. If not, please report the issue.

#. Open Photoshop. Once it's running, double-click both files to load them.

   Photoshop should activate each time, though initially, it might appear as if nothing has changed.

#. To verify the installation, go to your Actions window, typically located on the right side. If it's not visible, go to :menuselection:`Windows --> Actions` or press :kbd:`Alt-F9`.

   You should see a few folders, two of which will have the same names as the files you double-clicked:

   * :file:`MiniMap 1024x2.atn`
   * :file:`MiniMap 1024x4.atn`

If these files are present, they should be installed. If not, please ask for assistance. Now, let's install the BF2 Editor files:

#. Navigate to :file:`C:\\Program Files (x86)\\Project Reality\\Project Reality BF2`.

   This path might differ if you installed the game on a different hard drive or in a custom location.

#. Open the BF2 folder within the :file:`.zip` file. You will find two files:

   * :file:`makeMegaMap_1024x2.con`
   * :file:`makeMegaMap_1024x4.con`

#. Extract these files into the ``Project Reality BF2`` folder.

Close Photoshop, as you won't need it for a while. Then, open the BF2 Editor and load your preferred mod. Once loaded:

#. Go to :menuselection:`Tools --> Options --> Miscellaneous`.
#. In the window that appears, you will see several input fields. Enter the following paths:

.. describe:: CustomCommandFile1

   Set this to: :file:`C:\\Program Files (x86)\\Project Reality\\Project Reality BF2\\makeMegaMap_1024x4.con`

.. describe:: CustomCommandFile2

   Set this to: :file:`C:\\Program Files (x86)\\Project Reality\\Project Reality BF2\\makeMegaMap_1024x2.con`

Now, open the BF2 Editor and load your map using the Level Editor to begin.

Basic MiniMap (Temporary/Preview Use)
-------------------------------------

If you're unfamiliar with creating a basic minimap, I'll explain the process now. It's often beneficial to generate a temporary minimap to preview its appearance before committing to extensive work, especially for larger maps. This temporary minimap is also useful for test builds. Once your map is finalized, you can replace it with your "perfect" final minimap. To create one, open your map in the level editor and navigate to the :menuselection:`Editor --> General` bar on the right.

Clicking the "generate" button will likely require a few seconds of waiting, after which a small preview of the newly generated minimap will appear in the top-left corner of your main view.

   As you can observe, its current state is quite rudimentary, with many objects missing and only ground shadows visible. You can also use this minimap for navigation; a small green box indicates your camera's current location. Clicking a different spot on the minimap will instantly teleport your camera there. It is not recommended for use as a navigation tool because it obscures the view. Generating and keeping a :guilabel:`2048x2048` image loaded somewhat defeats its purpose, but the option is available if required.

Once generated, this minimap is saved to your map's editor folder, overwriting any previous minimaps unless they were backed up.

Advanced Tweaks
---------------

The following steps will enhance the appearance of your minimap. Most of these adjustments have been integrated into the scripts you've already installed, eliminating the need for manual input each time. However, a few steps require manual execution before generating the final minimap.

.. note::

   **Do not** save any map changes made from this point onward. These modifications are solely for improving the minimap's appearance and may not necessarily enhance your map's overall quality.

#. The first adjustment involves your roads.

   Switch to the :guilabel:`Roads Tool`. Then, in the Editor bar on the right, click the :guilabel:`Build All Final Roads` Button.

   This action will precisely align your road textures with the terrain without altering the splines or the in-game appearance of the roads. The editor processes splines much slower when they are in this state, which is why it's not the default behavior. Essentially, this ensures that all roads on your minimap will appear on top of the terrain, never underneath.

   Once this is complete, exit the road tool and return to a tool like the move tool.

#. The second adjustment involves the water.

   When the minimap is rendered, the water level appears to rise by approximately :guilabel:`1m`. To ensure the minimap's water level matches the in-game level, you need to lower all water by :guilabel:`1m`.

   #. Navigate to :menuselection:`Tweaker Bar --> Map Settings --> Water Settings`.
   #. Reduce your :guilabel:`Sea Water Level` by :guilabel:`1m`.

   For example, if your original Sea Level was 26.8, it would become :guilabel:`25.8`.

   Remember, these changes are solely for correcting the minimap's appearance and will not be saved upon exiting the editor.

   If your map contains any water planes, you must also lower them by :guilabel:`1m`. The most efficient way to do this is to select all water planes on the map. Then, in the tweaker bar, check their current 'y' position (from the x, y, and z coordinates) and drag them down as close as possible to :guilabel:`1m` below their original position.

#. The third adjustment involves making all overgrowth appear as static objects on the map.

   This ensures that overgrowth is drawn on your minimap in its actual position. Adjusting the overgrowth draw distance will reposition all overgrowth, causing it to no longer align with the terrain shadows.

   To achieve this, you only need to lightmap a single object on the map. While this method may not work for all users, it typically requires having sample files in your mod path. If you have the Project Reality lightmap samples installed, this should not be an issue.

   It's best to select a very simple, small object for relightmapping.

      I consistently choose the :guilabel:`1m` crate whenever possible. Simply select it, then go to :guilabel:`Trace Selected Item(s)`, and lightmap it at its previous quality setting (it should be final unless there's a specific reason otherwise).

   Once the lightmaps for that object are complete, you should observe that all overgrowth on your map has transformed into static overgrowth. However, you should have had your overgrowth turned off previously for this check.

      A good way to verify this is to drag a selection box around the overgrowth. If you can select it and you didn't place it manually, then it's working correctly.

#. The fourth step, depending on your map, is to activate its texture mode.

   * Many static objects, such as tents, have Desert and Woodland textures (and potentially others) that you'll want to display on your minimap, just as they appear in-game.
   * Some maps might also use custom textures for large objects that will be visible and make a difference on the minimap; you will need to load these.

      For example, Muttrah uses its own textures to render all buildings in a distinct white, mirroring their real-world appearance. I will need to load these for this process.

   * Therefore, you simply need to load the appropriate Texture Suffix, and you're ready.

#. Finally, switch to :guilabel:`Detail Texture Mode` (if you are not already in it) by navigating to :menuselection:`Render --> Detail Texture Mode`, or by pressing :kbd:`Ctrl-F4` (be careful not to press :kbd:`Alt-F4`, as that will close the editor).

.. note::

   *AFsoccer*: If you encounter issues after lightmapping an object (such as the crate mentioned by Rhino), an alternative is to lightmap the nearest terrain grid. For example, if lightmapping an object causes your cursor to display numerous move arrows or prevents you from moving your screen, try lightmapping the terrain using :guilabel:`terrain/primary/closest/final` as your settings. You should back up your existing terrain lightmaps so you can replace them with the one you are about to create. This process will achieve the desired result, and the new terrain shadows will not become visible until you reopen the map, ensuring the minimap appears correctly.

Generating The Minimaps
-----------------------

The process for generating minimaps varies depending on your map's size. You will follow one of these paths:

   :A: For 256x2 (0.5km²) and 512x2 (1km²) sized maps.
   :B: For 1024x2 (2km²) sized maps.
   :C: For 1024x4 (4km²) sized maps.

256x2 (0.5km²) and 512x2 (1km²) Sized Maps
   This step applies to :guilabel:`256x2 (0.5km²)` and :guilabel:`512x2 (1km²)` maps. If you use this method for larger maps, some objects may be omitted during minimap generation. However, it remains a viable alternative if you lack sufficient RAM to generate very large minimaps using other methods.

   Unlike options :guilabel:`B` and :guilabel:`C`, I cannot automatically insert a series of commands for you just before minimap generation, as we will deviate from the editor's standard creation process with a few adjustments.    First, you will need to manually enter these additional commands into the console to improve object rendering and appearance:

   .. describe:: renderer.minCullDistance

      Set this value to ``2000`` to ensure objects are fully rendered during minimap generation.

   .. describe:: staticMeshRenderer.noLods

      Set this value to ``1`` to disable Level of Detail (LOD) processing during minimap generation.

   After entering these commands, generate your minimap using the standard editor script by clicking the :guilabel:`Show` button in the minimap editor bar.

   Now, proceed to the **Editing The MiniMaps** section.

1024x2 (2km²) Sized Maps
   This step is specifically for :guilabel:`1024x2 (2km²)` maps. Using it for maps of different sizes may not yield optimal results. While untested, it is theorized that it could either omit parts of the map or include surrounding terrain, leading to inaccuracies.

   This process is largely similar to option B, with one key difference: you must execute a distinct minimap generation script.

   .. note::

      This particular step is memory-intensive, as you will be generating **4** separate minimaps.

      To proceed (assuming you have completed the setup in Step 1):

      Select :menuselection:`Tools --> Custom Action --> Execute Custom Command File 2 [C:\\bla bla bla\\makeMegaMap_1024_2.con]`.

1024x4 (4km²) Sized Maps
   This step is intended for :guilabel:`1024x4 (4km²)` maps. Applying it to maps of different sizes may not produce satisfactory results. While untested, it is theorized that it could either omit portions of the map or include surrounding terrain, leading to inaccuracies. This process is largely similar to option :guilabel:`C`, with one minor distinction: you must execute a different minimap generation script.

   .. note::

      This step demands significant RAM, as you will be generating **16** distinct minimaps.

      To proceed (assuming you have completed the setup in Step 1):

      Select :menuselection:`Tools --> Custom Action --> Execute Custom Command File 1 [C:\\bla bla bla\\makeMegaMap_1024_4.con]`.

Editing The MiniMaps
--------------------

In this section, we will edit the minimaps to achieve the best possible appearance.

First, it is advisable to exit the BF2 editor. If you have been working on a 4km map, it's probably a good idea to restart your computer before proceeding.

This section will again be divided into parts A, B, and C, based on different map sizes:

   :A: For 256x2 (0.5km²) and 512x2 (1km²) sized maps.
   :B: For 1024x2 (2km²) sized maps.
   :C: For 1024x4 (4km²) sized maps.

256x2 (0.5km²) and 512x2 (1km²) Sized Maps
   For these map sizes, you only need to perform basic edits to the minimap, primarily if you wish to enhance the appearance of water. These adjustments largely depend on your Photoshop skills.

   Open the :file:`minimap.dds` file, located at :file:`/levels/*yourmap*/editor/minimap.dds`, using Photoshop. Apply any desired Photoshop edits to improve its appearance (avoid using filters). Once done, you can proceed directly to Step 6.

1024x2 (2km²) Sized Maps
   For this map size, you must combine the **4** minimaps generated. You can use the provided Photoshop batch files or perform this manually. Afterward, you will need to blend in any water features on the map.

   With Photoshop open (and the Action files installed, as instructed in Step 1), open or create a small file. Any open file will suffice. Then, navigate to :menuselection:`File --> Automate --> Batch`. After this, save your work and proceed to Step 6.

   Once everything is configured, click :guilabel:`Ok` and allow the process to complete.

1024x4 (4km²) Sized Maps
   For this map size, you must combine the **16** minimaps generated. You can use the provided Photoshop batch files or perform this manually. Afterward, you will need to blend in any water features on the map.

   With Photoshop open (and the Action files installed, as instructed in Step 1), open or create a small file. Any open file will suffice. Then, navigate to :menuselection:`File --> Automate --> Batch`. After this, save your work and proceed to Step 6.

Saving The MiniMaps To Be Used In-Game
--------------------------------------

Now, we will save our minimaps in a format that minimizes performance impact while maintaining visual quality.

During gameplay, the minimap, like any other texture (e.g., a tank texture), must be loaded and stored in RAM. Saving the minimap in an incorrect format or at too high a resolution can lead to noticeable performance drops.

EA's minimaps are typically low-resolution, saved in DXT1 format at ``512x512``. However, they inexplicably include 10 MipMaps, which are unused and negatively affect performance. Despite this, their minimaps are only 170KB, which is negligible.

We will save our minimaps in DXT1 format, at ``1024x1024`` resolution, and without MipMaps. For ``1024x4`` maps, you might consider saving with the same settings but at ``2048x2048`` resolution. This will result in a 2MB minimap, offering the same detail as a ``1024x2`` minimap. The choice depends on how much you value the extra detail. However, for users with over 1024MB of RAM, an additional 2MB is usually insignificant. Note that reducing the size by half (e.g., from 2048 to 1024) reduces the file size by a quarter (e.g., from 2MB to 512KB). Regardless of the size you choose, your minimap's dimensions MUST be a power of ``2`` (e.g., ``16``, ``32``, ``64``, ``128``, ``256``, ``512``, ``1024``, ``2048``). Otherwise, a bug with ATI graphics cards may prevent them from properly rendering textures outside of these resolutions, causing display issues.

The first step is to decrease the size of our MiniMap to ``1024x1024`` or ``2048x2048``.

#. Go to :menuselection:`Image --> Image Size` at the top of the screen. This will open a new window.
#. In this window, enter your desired new :guilabel:`Width` and :guilabel:`Height` in pixels, then allow the program to process the change.
#. Now it's time to save your minimap. Go to :menuselection:`File --> Save As`.
#. Browse to :file:`/levels/*your map*/Hud/Minimap/`. In this folder, you will see three :file:`.dds` files.

   If you do not see them, change the format filter to D3D/DDS ``*.DDS``:

   .. describe:: ingameMap.dds

      This is the primary minimap visible to all players.

   .. describe:: commanderMicromap.dds

      * This minimap was originally intended by DICE for the commander's view but was never fully implemented.
      * DICE likely decided against its full implementation later in development and did not completely remove it.
      * Like many other elements in BF2, it's best not to delete it, it *might* cause a Crash To Desktop (CTD), though this has not been thoroughly tested.

   .. describe:: commanderMap.dds

      * Another unused minimap that DICE planned for the commander's view.
      * Similar to the micromap, it was likely abandoned during development and not fully removed.
      * As with other BF2 elements, it's advisable not to delete it, as it *might* cause a CTD, though this hasn't been extensively tested.

Now, back to saving!

#. Save the :file:`ingameMap.dds` file.

   Double-click it to overwrite the existing file, ensuring you match the DDS settings provided below.

   While you could leave the other two minimaps as they are, it's best practice to resize them to 32x32 pixels, using the same DDS settings as above. Save them over the existing files to reduce your map's overall size. This makes them only **1KB** each and keeps them in place, just in case deleting them would cause a CTD (though it's unlikely, this method is as effective as deleting them).

#. Package it with your map.

You have now successfully created a "perfect" minimap for your map.

`Here you can find the Grid overlay used on PR maps <https://www.realitymod.com/forum/f354-community-maps/133780-map-grid-overlay-template.html>`_
