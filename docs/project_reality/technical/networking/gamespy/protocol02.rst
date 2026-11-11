
Protocol 02: Echo
=================

An echo protocol. The server always returns the data sent after the protocol ID (up to 32 bytes) prefixed with the Echo Response Identifier (0x05).

Request
-------

FE FD 02 XX\ :sup:`0` ... XX\ :sup:`31`

Reply
-----

05 XX\ :sup:`0` ... XX\ :sup:`31`
