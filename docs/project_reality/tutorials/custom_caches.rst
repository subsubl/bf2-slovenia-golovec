
Setting Custom Cache Amounts
============================

Configure custom cache amounts for your maps using the following method.

In your :file:`init.con` file, set the number of caches for the specific map layout you wish to modify. This follows the same method used to adjust tickets in AAS.

.. code-block:: text

   gameLogic.setDefaultNumberOfTicketsEx <layer> <insurgent team> <caches>

The maximum number of caches is 10. Values exceeding this will revert to the default amount defined in :file:`realityconfig_public.py` (currently 5).

Example
-------

For example, on the map Sbeneh, the MEC faction often finds Insurgency mode challenging. To balance this, adjust the settings so that only 3 caches must be destroyed across all layouts:

First, create a new :file:`init_ins.con` file. Include this file at the beginning of all insurgency GameplayObjects (:file:`gamemodes/gpm_insurgency`) using the following command:

.. code-block:: text

   run ../../../Init_ins.con

Then, set the cache amount in the new :file:`init_ins.con` file:

.. code-block:: text

   gameLogic.setDefaultNumberOfTicketsEx 32 1 3
   gameLogic.setDefaultNumberOfTicketsEx 64 1 3
   gameLogic.setDefaultNumberOfTicketsEx 128 1 3

You can also modify BlueFor tickets, similar to AAS adjustments. For new maps and layers, retain the default of 5 caches and only change this value after thorough testing on public servers.

When setting custom cache amounts for a layer, apply these settings to all layers—even those intended to use the default amount—to prevent bugs during consecutive layer play.
