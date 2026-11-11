
Adding Light Effects to Maps
============================

:Original Author: Hfett

.. important::

   The original version contains images that are no longer available.

This tutorial describes how to create lighting effects in the editor.

.. seealso::

   For an example of night map lighting effects, refer to the following video: https://www.youtube.com/watch?v=TYhI2fjdEqI

Prerequisites
-------------

* Map loaded in the editor.
* Basic understanding of editor tools.

Lighting Sources
----------------

Lighting sources are manipulated similarly to static objects. They primarily affect other static objects within the editor, although they also affect overgrowth and undergrowth entities in-game. For optimal visibility, place light sources near static objects.

Glow Objects
^^^^^^^^^^^^

The following objects, located in :file:`/objects/common/glow`, generate visible light orbs.

.. describe:: glow6

   A large light source, useful for general illumination.

.. describe:: glow3

   A small light source, suitable for guard towers, buildings, and entrances.

.. describe:: glow5

   A large red orb.

Light Sources
^^^^^^^^^^^^^

The following objects, located in :file:`/objects/common/lightsources`, provide more focused illumination.

.. describe:: Baselight

   A smaller light source, appropriate for interiors (e.g., lamps or lightbulbs).

.. describe:: Houselight big

   A larger light source, used to simulate more intensive light from a single source.

Creating an Illuminated Interior
--------------------------------

#. Place the desired structure (e.g., a shack).
#. Place a light fixture (e.g., a lamp from the :file:`/miscobjects` folder or a lightbulb from :file:`/staticobjects/common`) inside the structure.
#. Place a light source (e.g., :file:`Baselight` or :file:`xp1_dayglowlight` from :file:`/staticobjects/pr/lightsources/`) a short distance below the light fixture.
#. Adjust the position of the light source to achieve the desired illumination effect.

.. note::

   The :file:`xp1_dayglowlight` provides stronger illumination than :file:`Baselight`.
