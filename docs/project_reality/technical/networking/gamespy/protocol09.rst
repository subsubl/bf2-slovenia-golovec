
Protocol 09: Echo Alternative
=============================

According to game-spy specifications this should be used to generate a 4 bytes value for us to send in the following replies as the TimeStamp, therefore allowing an IP verification.

Battlefield 2 however just returns 4 bytes of what we send with 2 more hardcoded bytes appended.

Request
-------

.. code-block:: text

   FE FD 09 XX XX XX XX

Reply
-----

.. code-block:: text

   09 XX XX XX XX 30 00
