
Common Issues & Errors
======================

RendDX9 Error
-------------

.. rubric:: Intel Core

For PCs or Laptops with a Dedicated Graphics Card:
   #. Go to :menuselection:`Windows Settings --> Graphics Settings`.
   #. Set :file:`prbf2.exe` to use the :guilabel:`Discrete GPU`.

For PCs or Laptops without a Dedicated Graphics Card:
   Update your Intel Xe/ARC Graphics driver.

   .. seealso::

      :download:`https://www.intel.com/content/www/us/en/download/785597/intel-arc-iris-xe-graphics-windows.html`

.. admonition:: This issue is common on the following systems:
   :class: warning

   * Intel Core 11th generation and newer
   * Intel N100 and other N-series processors
   * Pentium G7xxx series
   * Intel ARC Alchemist dedicated graphics cards

``memory.dll`` Crashes After Play Sessions
------------------------------------------

This issue occurs due to unknown differences in how GPU drivers manage memory. This is why some players may not experience this error at all.

.. rubric:: Experimental Fix

Use DXVK and enable the setting ``d3d9.deviceLossOnFocusLoss = True``. DXVK has its own memory mapping system, which makes longer gaming sessions less likely to crash. However, there are still some bugs with DXVK, so this fix is considered experimental.

.. admonition:: Download

   :download:`https://github.com/doitsujin/dxvk`

Cannot Hear Anything
--------------------

* Turn off positional audio in Mumble's settings.

  This might help, or it might not.

* Connect your headphones using the included USB cable.
* Purchase a backup wired audio device specifically for PR.

  I personally suggest inexpensive Chinese in-ear monitors for PR.

Performance Slowly Degrades Overtime
------------------------------------

* Your computer might need a thorough cleaning and new thermal paste.
* Set a more aggressive fan curve to maintain high CPU turbo clock speeds.

Low Performance on Ryzen CPUs
-----------------------------

#. Enable :guilabel:`CPPC` and :guilabel:`CPPC`\-preferred cores.
#. Enable :guilabel:`CPB` (Core Performance Boost) and :guilabel:`PBO`.
#. Go to :menuselection:`BIOS' advanced menu --> AMD CBS --> Zen/CPU common options menu`.
#. Enable the following options:

   * :guilabel:`L1` & :guilabel:`L2` Cache Hardware Prefetcher
   * :guilabel:`Streaming Stores Control`
   * :guilabel:`OPcache Control`

Launched Into an Infinite Black Screen
--------------------------------------

* Make sure no third-party antivirus software is blocking PR.
* Start PR using an offline profile. If this works, there might be a problem with your network. Try using a VPN or contact your internet service provider (ISP).

Stuck on "Joining Server"
-------------------------

.. rubric:: This can be caused by several different issues.

Network issue on the player's side:
   * Switch to a wired Ethernet connection.
   * Try using a VPN.
   * Contact your internet service provider (ISP) to report the issue.

PR is installed on an external drive that is not formatted as NTFS:
   Reformat your drive to NTFS or move the game back to your internal drive.

Persistent Skipping/Stuttering
------------------------------

.. rubric:: Possible Solutions

* Switch to a wired Ethernet connection.
* Upgrade to a newer WiFi protocol that operates at a higher frequency.

  Ensure that both your router and your PC/laptop support the newer protocol!

.. admonition:: If you cannot do either of those:

   * Make sure your WiFi is on a less-used channel.
   * Increase your transmit power.
