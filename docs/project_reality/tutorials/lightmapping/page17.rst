
Optimizing "Flat" Lightmaps
===========================

If your map contains significant sea water, you will likely have several "flat" lightmaps—textures consisting of a single solid color representing a flat sea surface. These can be optimized to save resources.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000478.jpg
   :align: center

.. warning::

   Having a 683kb texture of just flat white is quite a waste, especially when you have multiple ones all adding up together. In my case, I have a total of 46 blank patches, which currently use 30.6MB of memory for nothing.

   Wasted file space is not just about download size; it primarily impacts the player's RAM usage. All of these textures must be loaded into RAM. Since BF2 is a 32-bit game, there is a limit to how much a player can load. Additionally, processing large textures, even if they are blank, can slow down FPS and overall performance. These can be optimized without any adverse effects.

To identify which patches are used and which are blank, overlay a patch grid onto your terrain lightmap.

#. Save your compiled terrain lightmap as a :file:`.psd` file (e.g., :file:`_TERRAINLightingMap_Patches.psd`).

   .. warning::

      If you are working with a 4km map and your terrain lightmap is :guilabel:`8192x8192`, resize it to :guilabel:`4096x4096` before proceeding.


   .. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000479.jpg

   .. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000480.jpg

#. Navigate to :menuselection:`Image --> Image Rotation --> Flip Canvas Vertical` to orient the lightmap as the game reads it, ensuring patches are in the correct order.

   .. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000481.jpg

   .. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000482.jpg

#. Download the :download:`Terrain Patch Grid <http://realitymod.com/rhino/editor/terrain_patch_grid.png>`.
#. Open it in Photoshop and duplicate it over your :file:`_TERRAINLightingMap_Patches.psd` image.

   .. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000483.jpg

   .. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000484.jpg

You should end up with something like this:

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000485.jpg
   :align: center

If you are working with a 1km map and have a terrain lightmap size of :guilabel:`2048x2048`, this patch should also duplicate over your image correctly, with its 4x4 (16 patch) setup.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000486.jpg
   :align: center

You can now clearly see what is in each patch. Many patches may be blank. For example, in my case, the following patches are used:

.. code-block:: text

   tx02x03, tx02x04, tx03x03, tx03x04, tx03x06, tx03x07, tx04x02, tx04x03, tx04x04, tx04x07, tx05x03, tx05x04, tx05x07, tx06x00, tx06x03, tx06x07, tx07x00, tx07x07

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000487.jpg
   :align: center

Some patches, like :file:`tx06x02`, may contain tiny variations in water transparency due to small hills under the water.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000488.jpg
   :align: center

Once you have identified the files you want to optimize, close all images in Photoshop and open only the files you intend to process.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000490.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000489.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000494.jpg
   :align: center

#. Click on the :guilabel:`Actions` tab (:menuselection:`Windows --> Actions`).
#. Click the :guilabel:`Create new set` icon and name it :guilabel:`Resize`.
#. Click the :guilabel:`Create new Action` icon and name it :guilabel:`8x8 DDS DXT1`.
#. Click the :guilabel:`Record` button. All subsequent steps will be recorded.

   .. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000495.jpg

   .. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000496.jpg

   .. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000497.jpg

   .. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000498.jpg

#. Navigate to :menuselection:`Image --> Image Size` and change the dimensions to :guilabel:`8x8 px`.
#. Navigate to :menuselection:`File --> Save As`. Select :guilabel:`DXT1 RGB 4bpp | no alpha` DDS format and enable :guilabel:`Generate MIP Maps`. Ensure :guilabel:`All` is selected in the dropdown.
#. Click :guilabel:`Save`, then close the image (:menuselection:`File --> Close`).
#. Click the :guilabel:`Stop Recording` button.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000499.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000500.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000501.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000502.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000503.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000504.jpg
   :align: center

If you open an optimized image in NVIDIA WTV, it should appear as an 8x8 DXT1 DDS image with 4 mipmaps and a total memory usage of approximately :guilabel:`0.1kb`.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000505.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000506.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000507.jpg
   :align: center

To apply this action to all opened files, use the Batch command:

#. Navigate to :menuselection:`File --> Automate --> Batch`.
#. In the :guilabel:`Play` section, select your newly created set and action. Set the source to :guilabel:`Opened Files`.

   .. warning::

      Ensure only the files you intend to optimize are open in Photoshop to avoid unintended modifications.

#. Click **OK** to begin the batch process.

   .. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000508.jpg

   .. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000509.jpg

After processing, the same images that previously used **30.6MB** will now use only **8.26KB**, significantly improving performance and reducing the player's RAM footprint.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000510.jpg
   :align: center
