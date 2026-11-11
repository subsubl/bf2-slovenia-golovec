GameSpy Protocol
================

Battlefield 2 utilizes the GameSpy SDK for server communication, handling tasks like server browsing, heartbeat, and status queries. All communication is performed over UDP, with packets limited to 1400 bytes.

General Format
--------------

Most GameSpy protocols share a common header format for identification and timestamping.

.. list-table:: Common Header (0xFE 0xFD)
   :header-rows: 1

   * - Field
     - Size
     - Description
   * - Header
     - uint16
     - Always ``0xFE 0xFD``.
   * - Protocol ID
     - byte
     - Identifies the specific sub-protocol.
   * - Timestamp
     - uint32
     - Used to distinguish between multiple packets from the same server.

Protocols Overview
------------------

.. list-table::
   :header-rows: 1

   * - Protocol
     - Purpose
   * - :doc:`basics`
     - Overview of the data types (Server, Player, Team) and key-value reporting format.
   * - :doc:`protocol00`
     - **Server Information**: Queries server headers, player details, and team stats via three sub-protocols (A, B, and C).
   * - :doc:`protocol02`
     - **Echo**: Simple protocol where the server returns up to 32 bytes of sent data.
   * - :doc:`protocol03`
     - **Heartbeat**: Sent by the game server to the Master Server every 60 seconds to signal availability.
   * - :doc:`protocol08`
     - **Keep Alive**: Sent by the Master Server to the game server to acknowledge its status.
   * - :doc:`protocol09`
     - **Echo Alternative**: Used for IP verification and generating timestamp values for subsequent replies.

.. toctree::
   :glob:

   basics
   protocol*
