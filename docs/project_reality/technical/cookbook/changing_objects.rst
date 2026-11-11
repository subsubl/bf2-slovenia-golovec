
Changing Objects At Runtime
===========================

:Original Author: Woody

Problem
-------

You might want to change how some of the standard Python code in BF2 works. For example, you might want to add your own RCon commands or modify how scores are tracked. While you *could* directly edit the default code, doing so extensively can lead to significant maintenance problems. It could also cause issues when applying future game patches from EA, as your changes might be overwritten.

Solution
--------

Python is a `dynamic language <https://en.wikipedia.org/wiki/Dynamic_language>`_, which means, among other things, that programs can modify themselves while they are running. We can use Python's dynamic nature to write code that changes the properties of standard BF2 objects during runtime.

Example: Adding A New Property To An Object
---------------------------------------------

Let's say you are developing a new mod for BF2 and need the :py:class:`bf2.PlayerManager.Player` class to track a new property called ``karma``. If you examine :py:class:`bf2.PhysicalObject`, you'll notice that Player Objects do not have a ``karma`` property, and you want to add one.

In Python, if your goal is simply to add a new attribute to an object, you can do it directly:

.. code-block:: python

   playerObject.karma = 0

That's it! If :py:class:`playerObject` is an instance of the :py:class:`bf2.PlayerManager.Player` class, we have just created a new attribute named ``karma`` within that specific instance and assigned it the value "0". There's nothing more to it—you can read and modify this attribute anywhere else in your code, just as if it had been part of the class definition from the beginning.

.. note::

   We did not add this attribute to the :py:class:`bf2.PlayerManager.Player` class itself.

   Instead, we added it to a specific instance of that class. This means only that particular player will have a ``karma`` attribute. If you want other players to have a ``karma`` attribute, you need to find their ``playerObjects`` and apply the same change.

   Assuming you have imported :doc:`bf2 <../python/reference/bf2>`, you could assign a karma attribute to all players by doing something like this.

   .. code-block:: python

      for playerObject in bf2.playerManager.getPlayers():
         playerObject.karma = 0

Discussion
----------

This cookbook entry only briefly introduces what you can achieve with dynamic code modification. Before you start making direct changes to BF2's default Python code, consider whether an approach like this might be cleaner and more manageable.

It might occur to you that *something* needs to be running to make these dynamic modifications. How does that *something* start running without itself modifying some of the standard code? The short answer is that these dynamic programming techniques are only possible if there's a "hook" you can use to trigger this and other code. DICE did not include such a hook in their Python code. Therefore, at least **one** modification must be made to the standard BF2 code: at a minimum, an "import" statement needs to be added to one of the main files to ensure your code is loaded and executed... but that's a topic for another time.
