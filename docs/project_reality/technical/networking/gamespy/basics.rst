
Basics
======

These are the protocols used to communicate with the server using the sv.gameSpyPort port in order to retrieve one or more of the following available information type:

Server Data
   This is general information about the game in progress (i.e., the map that is being played, the type of game, and any specific game settings that would be of interest to players before they joined).

Player Data
   This is information about a specific player that is in the current game (i.e., the player's name, their current score, what team they are on, and the latency to the game server).

Team Data
   This is information about a specific team in the current game (i.e., the name of the team and the team score. If your game does not support team play you do not need to report any team information).

.. code-block:: text

   Data is reported in a "key-value" format: player keys always end in an "_" character (such as "score_") and team keys always end in a "_t" (such as score_t). Server keys can end in anything other than an "_" or "_t"

.. code-block:: text
   :caption: Almost every protocol starts the same way:

   0xFE 0xFD YY XX XX XX XX

.. list-table::
   :stub-columns: 1

   * - Header
     - Protocol
     - TimeStamp
   * - uint16
     - ID byte
     - uint32
   * - Always 0xFE 0xFD
     -
     - Always retuned in the messages, may be used as an identifier distinguish between multiple packets from the same server

App packages sent by the server are limited to 1400 bytes and all communication is handled in UDP

Battlefield 2 uses the Gamespy SDK to handle these requests.
