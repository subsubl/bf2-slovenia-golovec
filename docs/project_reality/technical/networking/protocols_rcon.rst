
The RCon Protocol
=================

Basics
------

This document outlines the RCON ("Remote Console") protocol used by the Battlefield 2 server. RCON operates as a TCP service, typically on port 4711. The BF2 server's TCP listener and RCON protocol are entirely implemented in Python, within the administrative module. You can find a description of how the administrative module handles RCON :doc:`here <../admin/module>`.

Banner
------

When a client connects, the server sends a header that ends with /n/n (two 0x0A characters). One of the lines in this header will be prefixed with the text (without quotes), "### Digest seed:". The value that follows the colon and space must be saved for the login process. Here is an example banner:

.. code-block:: console

   ### Battlefield 2 default RCON/admin ready.
   ### Digest seed: dOrdNsTRDWSvPWXi

Commands
--------

All commands sent by the client must have /n (0x0A) appended to them to indicate the end of the line. An optional 0x02 character can be added before the command. This tells the server to append a 0x04 character to the command's output, signaling the end of the data. However, it's important to note that the server does not send a 0x0A (newline) character after the 0x04 (End of Transmission) character, so your program must be able to handle this. This is an optional part of the protocol that you can implement if it's important for your environment to receive all of the output.

The :file:`remoteconsole.py` sample script included with BF2 uses the 0x02 character for all commands by default. All examples provided below do not include the 0x02 and 0x04 characters.

Login
-----

An MD5 hash of the password, using the `MD5 algorithm <https://en.wikipedia.org/wiki/MD5>`_, is calculated with the seed obtained from the banner. This hash is represented in hexadecimal format (e.g., ``106c9f3b52c173dc210e7ee612e689bb``). Note that the seed is not used in the typical seeding manner. To generate a valid hash, you combine the seed returned in the banner with the password, and then send this resulting hash to the server. For example, if the returned seed is ``PXYHKqLrFfENvONV`` and the RCON password is ``password``, the string to hash would be ``PXYHKqLrFfENvONVpassword``. In this specific case, it would produce a hash of ``bc3d874909af1404eec2765ef3613b19``.

A login command might appear as follows:

.. code-block:: text

   6c 6f 67 69 6e 20 62  64 32 39 39 37 39 30 64 64 login b d299790dd
   33 37 37 34 36 62 32  31 66 32 32 33 65 33 34 37 37746b2 1f223e347
   39 66 63 33 63 31 0a                             9fc3c1.

Possible responses from the standard BF2 RCON server include:

.. code-block:: text

   41 75 74 68 65 6e 74 69  63 61 74 69 6f 6e 20 66 Authenti cation f
   61 69 6c 65 64 2e 0a                             ailed..

.. code-block:: text

   41 75 74 68 65 6e 74 69  63 61 74 69 6f 6e 20 73 Authenti cation s
   75 63 63 65 73 73 66 75  6c 2c 20 72 63 6f 6e 20 uccessfu l, rcon
   72 65 61 64 79 2e 0a                             ready..

You must successfully authenticate before you can use other commands. Otherwise, you will receive the following message:

.. code-block:: text

   65 72 72 6f 72 3a 20 6e  6f 74 20 61 75 74 68 65 error: n ot authe
   6e 74 69 63 61 74 65 64  3a 20 79 6f 75 20 63 61 nticated : you ca
   6e 20 6f 6e 6c 79 20 69  6e 76 6f 6b 65 20 27 6c n only i nvoke 'l
   6f 67 69 6e 27 0a                                ogin'.

``exec``
--------

This command executes a server command (like a PunkBuster command) or retrieves/sets a server setting's value. For example:

.. code-block:: text

   65 78 65 63 20 73 76  2e 74 69 63 6b 65 74 72 61 exec sv .ticketra
   74 69 6f 0a                                      tio.

Response:

``31 30 30 0a 100.``

Example PunkBuster command:

.. code-block:: text

   65 78 65 63 20 70 62  5f 73 76 5f 70 6c 69 73 74 exec pb _sv_plist
   0a

Due to a bug (or intended 'feature') in the BF2/PunkBuster integration, PunkBuster commands will not return any text. Their output will instead be displayed on the server console itself or, if necessary, in the PunkBuster log files.

``users``
---------

This command displays the active users currently logged into the RCON system. To request this information, send:

``75 73 65 72 73 0a users.``

The response may vary depending on the RCON method being used (e.g., standalone client, in-game). Below is an example with two remote standalone clients:

.. code-block:: text

   61 63 74 69 76 65 20 72  63 6f 6e 20 75 73 65 72 active r con user
   73 3a 0a 74 63 70 3a 20  31 32 2e 33 34 2e 35 36 s:.tcp:  12.34.56
   2e 37 38 3a 36 32 33 35  32 0a 74 63 70 3a 20 38 .78:6235 2.tcp: 8
   37 2e 36 35 2e 34 33 2e  32 31 3a 36 32 32 34 38 7.65.43. 21:62248
   0a

Notes
-----

If a command you enter does not exist, you will receive the following message:

.. code-block:: text

   75 6e 6b 6e 6f 77 6e 20  63 6f 6d 6d 61 6e 64 3a unknown  command:
   20 27 62 6c 61 68 27 0a                           'blah'.
