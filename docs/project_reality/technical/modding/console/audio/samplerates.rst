
Mass-Converting Sample Rates
============================

:Original Author: [R-DEV] Arab

.. important::

   The original version has images that are not available anymore.

This tutorial explains the mass conversion of audio sample rates while preserving sound region markers.

Sound Forge 12 Pro Suite
------------------------

Sound Forge 12 Pro Suite is the recommended tool for this task because it preserves sound markers during conversion. It also maintains original mono and stereo settings, preventing engine strain caused by improper stereo conversion of mono audio files.

Loopable sounds, such as engine idle, automatic rifle firing, or helicopter rotors, retain their characteristics when sample rates are modified.

Identifying Sample Rates
------------------------

To view the sampling rate of :file:`*.wav` files in Windows Explorer:

#. Set the view to :guilabel:`Details` mode.
#. Enable the :guilabel:`Bit Rate` column:

   - Right-click a column header.
   - Select :guilabel:`More...`.
   - Check :guilabel:`Bit Rate` and click :guilabel:`OK`.

Use the following table to identify sample rates based on bit rates:

.. list-table:: Sample Rate Mapping
   :header-rows: 1

   * - Bit Rate
     - Sample Rate
     - Channels
   * - 176 kbps
     - 11.025 kHz
     - Stereo
   * - 352 kbps
     - 22.05 kHz
     - Mono
   * - 705 kbps
     - 44.1 kHz
     - Mono
   * - 768 kbps
     - 48 kHz
     - Mono
   * - 1411 kbps
     - 44.1 kHz
     - Stereo
   * - 1536 kbps
     - 48 kHz
     - Stereo

Alternatively, use tools such as :file:`MediaInfo` or :file:`Wave Agent Beta` to verify sampling rates, channel counts, and bit depths.

Converting from 44.1 kHz to 48.0 kHz
------------------------------------

Use the Batch Converter in Sound Forge Pro 12 Suite with the following configuration:

#. :guilabel:`Files to convert tab`: Add the target files.
#. :guilabel:`In Process tab`:

   - Select :guilabel:`Resample` from the :guilabel:`Menu` dropdown.
   - Click :guilabel:`Add Effect`.
   - Select the preset ``[Sys] Resample to 48,000 Hz with anti-alias filter``.
   - Select :guilabel:`Set the sample rate only (do not resample)`.
   - Click :guilabel:`OK`.

#. :guilabel:`Save tab`:

   - Click :guilabel:`Add Save Options`.
   - Set all three options to :guilabel:`Same as Source`.
   - Click :guilabel:`OK`.

#. Click :guilabel:`Run Job`.

Handling Low Sample Rates
^^^^^^^^^^^^^^^^^^^^^^^^^

When upsampling files below 44.1 kHz (e.g., 11.025 kHz or 22.05 kHz) to 48 kHz, use the ``Resample 2`` feature. The standard conversion settings (44.1 to 48) can reduce audio quality for these files.

.ogg Serialization
------------------

Battlefield 2 utilizes serialization to enable :file:`*.ogg` sound playback over a network, which is required for offline and online gameplay.

Converting :file:`*.ogg` files removes serialization, causing audio playback failure. To preserve serialization, convert :file:`*.ogg` files to :file:`*.wav` format in Sound Forge without resampling, then resample each sound file individually.
