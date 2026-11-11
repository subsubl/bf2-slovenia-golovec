
Default .desc File Configuration
================================

:Original Author: [R-DEV] Outlawz7 (Retired)

The Battlefield 2 Editor generates a default :file:`.desc` file in the :file:`Info` folder for each new map. These files often contain legacy content from the base game that is unnecessary for Project Reality.

The following XML configuration provides a clean, properly formatted :file:`.desc` template optimized for Project Reality. It supports all map sizes and game modes while excluding briefing entries and other extraneous content.

.. code-block:: xml

    <map>
        <name> YOURMAPNAMEHERE </name>
        <music> common/sound/menu/music/load/YOURMUSICHERE.ogg </music>
        <modes>
            <mode type="gpm_cq">
                <maptype players="16" type="aasinfantry" locid="GAMEMODE_DESCRIPTION_aasinfantry"></maptype>
                <maptype players="32" type="aasalternative" locid="GAMEMODE_DESCRIPTION_aasalternative"></maptype>
                <maptype players="64" type="aasfullassets" locid="GAMEMODE_DESCRIPTION_aasfullassets"></maptype>
                <maptype players="128" type="aaslarge" locid="GAMEMODE_DESCRIPTION_aaslarge"></maptype>
            </mode>
            <mode type="gpm_vehicles">
                <maptype players="16" type="vehiclewarfare" locid="GAMEMODE_DESCRIPTION_vehiclewarfare"></maptype>
                <maptype players="32" type="vehiclewarfare" locid="GAMEMODE_DESCRIPTION_vehiclewarfare"></maptype>
                <maptype players="64" type="vehiclewarfare" locid="GAMEMODE_DESCRIPTION_vehiclewarfare"></maptype>
                <maptype players="128" type="vehiclewarfare" locid="GAMEMODE_DESCRIPTION_vehiclewarfare"></maptype>
            </mode>
            <mode type="gpm_skirmish">
                <maptype players="16" type="skirmish" locid="GAMEMODE_DESCRIPTION_skirmish"></maptype>
                <maptype players="32" type="skirmish" locid="GAMEMODE_DESCRIPTION_skirmish"></maptype>
                <maptype players="64" type="skirmish" locid="GAMEMODE_DESCRIPTION_skirmish"></maptype>
                <maptype players="128" type="skirmish" locid="GAMEMODE_DESCRIPTION_skirmish"></maptype>
            </mode>
            <mode type="gpm_insurgency">
                <maptype players="16" type="insurgency" locid="GAMEMODE_DESCRIPTION_insurgency"></maptype>
                <maptype players="32" type="insurgency" locid="GAMEMODE_DESCRIPTION_insurgency"></maptype>
                <maptype players="64" type="insurgency" locid="GAMEMODE_DESCRIPTION_insurgency"></maptype>
                <maptype players="128" type="insurgency" locid="GAMEMODE_DESCRIPTION_insurgency"></maptype>
            </mode>
            <mode type="gpm_cnc">
                <maptype players="16" type="cnc" locid="GAMEMODE_DESCRIPTION_cnc"></maptype>
                <maptype players="32" type="cnc" locid="GAMEMODE_DESCRIPTION_cnc"></maptype>
                <maptype players="64" type="cnc" locid="GAMEMODE_DESCRIPTION_cnc"></maptype>
                <maptype players="128" type="cnc" locid="GAMEMODE_DESCRIPTION_cnc"></maptype>
            </mode>
            <mode type="gpm_coop">
                <maptype ai="1" players="16" type="coopinfantry" locid="GAMEMODE_DESCRIPTION_coopinfantry"></maptype>
                <maptype ai="1" players="32" type="coopalternative" locid="GAMEMODE_DESCRIPTION_coopalternative"></maptype>
                <maptype ai="1" players="64" type="coopfullassets" locid="GAMEMODE_DESCRIPTION_coopfullassets"></maptype>
                <maptype ai="1" players="128" type="coopfulllarge" locid="GAMEMODE_DESCRIPTION_coopfulllarge"></maptype>
            </mode>
        </modes>
    </map>

.. note::

   Customize the template by removing any unused game modes or map sizes to keep the configuration efficient.

Configuration Elements
-----------------------

.. describe:: <map>

   The root element of the ``.desc`` file. It contains the complete map configuration.

.. describe:: <name>

   Specifies the display name of the map.

.. describe:: <music>

   Specifies the path to the music file to be played during map loading.

.. describe:: <modes>

   A container element that holds all supported ``<mode>`` entries.

.. describe:: <mode>

   Defines a game mode configuration. It includes a ``type`` attribute specifying the mode (e.g., ``gpm_cq``).

.. describe:: <maptype>

   Defines the map settings for a specific player count within a mode. It uses the following attributes:

   #. ``players``: The number of players supported by this map type.
   #. ``type``: The internal technical identifier for the map type.
   #. ``locid``: The localization ID used to retrieve the mode's description.
   #. ``ai``: (Optional) Indicates whether the mode supports AI players.
