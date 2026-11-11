
Protocol 00: Server information
===============================

Sub-Protocol A
--------------

Only replies with 1 message, even if means responding with incomplete information

Request
^^^^^^^

.. code-block:: text

   0xFE 0xFD 0x00 XX XX XX XX HH PP TT 0x00

HH, PP and TT are a individual flags to request to the server its headers, players and team information, respectively.

These flags need to set to FF to be considered enabled and multiple combinations can be made, eg: asking headers and team information will be (FF 00 FF)

Reply
^^^^^

Same as ``Sub-Protocol B``'s reply but limited to 1 reply, 1400 bytes and some fields might be omitted, depending on the flags.

Sub-Protocol B
--------------

The most complete protocol; it always reply all 3 information fields (server, players, team) using one or more packages (of 1400 bytes).

Request
^^^^^^^

.. code-block:: text

   0xFE 0xFD 0x00 XX XX XX XX HH PP TT 0x01

HH, PP and TT will be ignored not matter the value.

It's the last byte, 0x01, that matters. More specifically the last byte only needs to have the least significant bit set to 1.

Reply
^^^^^

The server may reply with one or more messages if the information is bigger than the 1400 bytes limit.

These messages will always start with:

.. code-block:: text

   00 XX XX XX XX splitnum 00 YY PAYLOAD

.. list-table::
   :stub-columns: 1

   * - Protocol ID
     - Timestamp
     - "splitnum"
     - splitnum
     - Message Number
   * - byte
     - uint32
     - string
     - byte
     - byte
   * - Always zero
     - The value sent in the request
     - Always "splitnum"
     - Only seen **00** probably indicates how the strings are terminated
     - The most significant bit indicates if its the last message, all others are used for the message number

The payload 1st byte indicates the type: 00, 01 and 02 for Server Headers, Player information and Team Information, respectively.

Server Headers
""""""""""""""

key/value pairs.

.. code-block:: text

   00 <key 1> 00 <value 1> 00 ... <key N> 00 <value N> 00  00

Example.

.. code-block:: text

   \00hostname\00[PR v1.4.6.0] =]H[= HARDCORE GAMING - NA\00gamename\00battlefield2\00gamever\001.5.3153-802.0\00password\000\00

Which is...

.. code-block:: text

   hostname: "[PR v1.4.6.0] =]H[= HARDCORE GAMING - NA"
   gamename: "battlefield2"
   gamever: "1.5.3153-802.0"
   password: "0" (false)

Player information and Team Information
"""""""""""""""""""""""""""""""""""""""

Player and Team informations are stored into <key>:<array of values>.

With the actual format being.

.. code-block:: text

   QQ <key 1> 00 <offset> <value 1 + offset> 00 ... <value NN> 00 00 00

QQ is the type. With 0x01 indicating its Player information and 0x02 representing Team information.

Since the message may end before the array ends, the first value after each key is the <offset> that defines the index to start from.

Here is an example of the player information's section with 3 players.

.. code-block:: text

   \01 player_\00\00 =MD=shilijia\00>11< WangXi\00 a365476093\00\00score_\00\00191\00159\000\00\00ping_\00\0050\0033\0018\00\00\00

Which is:

.. code-block:: text

   player_: [" =MD=shilijia", ">11< WangXi", " a365476093"]
   score_: ["191", "159", "0"]
   ping_: ["50", "33", "18"]

Sub-Protocol C
--------------

The 3rd of our sub-protocols to request information about the server allows you to indicate which headers and how many you want to know about.

Request
^^^^^^^

.. code-block:: text

   0xFE 0xFD 0x00 XX XX XX XX YY KK0 ... KKYY-1 0x00 0x00

The 8th byte (YY) informs the server how many headers you're asking for, meaning the number of bytes that follows afterwards (plus 2 terminal ones). These following bytes, excluding the last 2, define the header's indexes that you're querying about. See next table to see the mapping between index and header.

.. csv-table::
   :header: "Offset", "Header"

   "01", "hostname"
   "02", "gamename"
   "03", "gamever"
   "04", "hostport"
   "05", "mapname"
   "06", "gametype"
   "07", "gamevariant"
   "08", "numplayers"
   "09", "??"
   "0a", "maxplayers"
   "0b", "gamemode"
   "0c", "??"
   "0d", "??"
   "0e", "??"
   "0f", "??"
   "10", "timelimit"
   "11", "roundtime?"
   "12", "??"
   "13", "??"

Reply
^^^^^

The sub-protocol C replies with the usual protocol ID followed by the provided timestamp, the payload and the null byte to terminate the message.

.. code-block:: text

   0x00 XX XX XX XX PAYLOAD 0x00

The payload consists in all header's value requested separated by 0x00. The header's values maintains the same order as in the request.

.. code-block:: text
   :caption: Example: Requesting the number of players and server name.

   0xFE 0xFD 0x00 0x20 0x21 0x21 0x20 0x02 0x08 0x01 0x00 0x00

The reply will be, 84 players and 'My Server':

.. code-block:: text

   0x00 0x20 0x21 0x21 0x20 0x84 0x00 [PR v1.4.17.0] My Server 0x00
