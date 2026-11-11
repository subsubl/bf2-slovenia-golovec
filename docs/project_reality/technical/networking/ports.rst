
BF2 Porting
===========

Preface
-------

Here is a list of common Project Reality Server Ports:

======== =========== ===================================================
Protocol Ports       Function
======== =========== ===================================================
TCP      80,443      Battle Recorder
TCP      22          SSH
TCP      4712        PRISM RCON
UDP      29901       Server status (GameSpy)
UDP      16567       Server Game Port
TCP      64740       Mumble (Block UDP, TCP works better for PR Mumble)
======== =========== ===================================================

Firewalling Your Server
-----------------------

The following information is from :file:`readmeserver.txt`:

::

   FIREWALL

   Using a software firewall on the server is not recommended,
   as it can negatively impact server performance and the overall
   gameplay experience.

How to firewall your server
~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. External firewall

   This involves having a separate machine through which all traffic must pass before reaching your server (my preferred method).

#. Local Firewall

   This means running a firewall directly on the same server as your game server (this uses local CPU resources, so it's not the most efficient approach).

We will NOT provide detailed instructions on how to set up a firewall for your system here, as many other websites cover this topic. Our focus here is to outline the specific rulesets required for a BF2 server to function correctly.

External Firewall
~~~~~~~~~~~~~~~~~

More information is needed here.

Local Firewall
~~~~~~~~~~~~~~

Linux Iptables
^^^^^^^^^^^^^^

This ruleset enables my server to appear in the server browser list, allows players to join and use VOIP, permits game administrators to connect via PRISM, and enables system administrators to connect using SSH.

.. note::

   This configuration is for a standard server with only one BF2 server running on the machine, and no unusual port usage. It is recommended that BattleRecorder be hosted on a separate system.

.. code-block:: console

   iptables -A INPUT -m udp -p udp -m multiport --dports 29901,16567 -j ACCEPT
   iptables -A INPUT -m tcp -p tcp -m multiport --dports 22,4711,64740 -j ACCEPT
