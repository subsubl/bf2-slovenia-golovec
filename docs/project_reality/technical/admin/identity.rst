
Player Identity
===============

In Battlefield 2, a player's identity can be represented in several ways. This page will discuss these methods, explain their different uses, and show you how to access and convert between them.

Player ID (index)
-----------------

The ``Player ID`` ("playerID", also known as "index") is the simplest and most fundamental way to identify players and is frequently used throughout the game. The first player to connect to the server receives a Player ID of "0", the second receives "1", and so forth. At the start of each new round, the server reassigns Player IDs to all players, beginning again at 0. This process fills any gaps in the numbering system caused by players who have disconnected.

Most :doc:`console commands <../modding/console/index>` that interact with players use the Player ID. For instance, ``admin.kickPlayer`` requires a Player ID number. The easiest way to determine which player has which Player ID from the console is to use the ``admin.listplayers`` command.

In Python, several methods are available to access player information using their Player ID. For example, :py:meth:`bf2.playerManager.getPlayerByIndex` takes a playerID and returns the corresponding playerObject.

Player Name
-----------

This is the name displayed in the colored "name tag" above each player's head in the BF2 game world. It is also the "account name" that players use to log into BF2. Since players must create an account for multiplayer internet play, EA's account management system ensures that each Player Name is unique. However, there is nothing to prevent a single player from registering multiple Player Names.

.. code-block:: python
   :caption: How to find a player's name from their Player Object

   playerObject.getName()

As of BF2 version 1.03, this method returns both the player's name and their 'prefix', which is an arbitrary tag up to 6 characters long. The regular expression ``\S{0,6}\s`` can be used to match the entire prefix of a player's name for removal or other purposes. A less precise but equally effective regex is ``\S.*?\s``.

Player Object
-------------

Player Objects ("playerObjects") are instances of the :py:class:`bf2.PlayerManager.Player` class. Each Player Object contains and provides access to a lot of information about a specific connected player. PlayerObjects are created when a player first connects to a running BF2 server and exist until that server shuts down. Even if a player disconnects, BF2 keeps their Player Object. If the same player reconnects later, BF2 tries to link them with their original Player Object.

If you need to find out a player's name, score, ping, or other details, you can use the methods available through their Player Object.

Soldier Object
--------------

Player Objects are abstract representations in the BF2 world, similar to the "spirit" or "ghost" of a player. In contrast, Soldier Objects ("soldierObjects") are instances of the :py:class:`soldierObject` class and represent "physical" objects within the BF2 world. These include geographic coordinates, orientation, and the ability to contain or be contained by other physical objects. When a player enters a game, a new Soldier Object is created and linked to their Player Object. If a player dies, the Soldier Object is destroyed, but the Player Object remains until the player respawns into the game.

If you need to determine a player's location, their current kit and weapon (which are "child" objects contained within the Soldier Object), or the vehicle they are using (a "parent" object that contains them), you should examine the player's Soldier Object.

.. code-block:: python
   :caption: How to find the Soldier Object that corresponds to a specific spawned-in player from their Player Object

   playerObject.getVehicle()

Apart from searching through all available players, there is no direct way to go from a Soldier Object to its corresponding Player Object. Instead, most :doc:`game events <../python/reference/events>` that would require this information send **both** the relevant Player Object and Soldier Object in their callbacks.

PlayerID (Hash)
---------------

This PlayerID, previously known as CDKey and hash, should not be confused with the index PlayerID.

This number provides a unique identification for players to the master server. Each Steam login is linked to a 32-digit, 128-bit hexadecimal number. When logging into the PR server, the MSProxy_ connects to the master server to authenticate the user's account. It then returns a verified or unverified value to the proxy. The PlayerID is recorded in connection logs, ban logs, and ban lists, and is used to identify accounts that may have multiple usernames. The commands !banid, !timebanid, and !unbanid use a PlayerID to manually ban or unban a player.

.. _MSProxy: https://gitlab.com/realitymod/public/prserverproxy/

In Python, the PlayerId can be accessed using :py:class:`realityserver.getPlayerHash` and is mainly used within the ban system.

Example hash: ``ec74c4b5dcc40a1962cfd61e1d062ea3``

IP Address
----------

An `IP address <https://en.wikipedia.org/wiki/IP_address>`_ is a unique identifier for a specific computer on a network, for example, ``192.168.100.1``. Generally, a player's IP address can help identify their computer (similar to how a CD key hash works) and provide information about their geographical location, such as their country. However, it's important to be cautious when using IP addresses for these purposes. Many internet service providers use `NAT <https://en.wikipedia.org/wiki/Network_address_translation>`_ to dynamically change their customers' IP addresses daily. AOL, for instance, changes addresses with each new connection. If you ban or kick a player based on their IP address, they might reconnect to your server a few minutes later with a different IP address.

.. code-block:: python
   :caption: How to access the IP address a player is using from their Player Object

   playerObject.getAddress()
