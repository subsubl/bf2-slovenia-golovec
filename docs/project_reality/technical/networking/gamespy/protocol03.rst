
Protocol 03: HEARTBEAT
======================

Packet sent by the game server to the Master Server every 60s with the server's information.

Request
-------

There is no request. Servers send this information every 60s so they can be considered 'alive' and thus displayed in the server browser.

Reply
-----

.. code-block:: text

   0x03 XX XX XX XX <localIPs> <port> <natneg> <stateChanged> <gamename> <publicInfo> <serverKeys>

localIPs
^^^^^^^^

Present when there's at least one local IP available.

A list composed by strings. Each string starts with 'localip' followed by a (sequential) number, a null character, and the the IP in IPv4 dotted-decimal notation, eg:

.. code-block:: text

   localip0 0x00 192.168.1.3 0x00 localip1 0x00 192.168.1.4 0x00 (42 bytes)

port
^^^^

Always available.

String literal localport folowed by the string representation of the integer that represents the port, eg:

.. code-block:: text

   localport 0x00 29900 (15 bytes)

Unkown
^^^^^^

- natneg
- stateChanged
- gamename
- publicInfo
- serverKeys
