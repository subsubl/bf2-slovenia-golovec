
Converting Destroyable Objects to Non-Destroyable Objects
=========================================================

:Original Author: [R-DEV] AFsoccer (Retired)

To convert a destroyable object to a non-destroyable object, follow these steps to create a modified version of the object's configuration files.

#. **Duplicate Files**: Create a copy of the original :file:`.con` and :file:`.tweak` files in the same directory. Append a :file:`_nondest` suffix to the names of the new files (e.g., :file:`stonebridge_nondest.con` and :file:`stonebridge_nondest.tweak`).
#. **Configure the .con file**: Open the new :file:`_nondest.con` file.

   Modify the object template name in each line, except for the lines specifying the collision mesh and geometry, which must continue to reference the original destroyable static mesh.

   Change ``ObjectTemplate.create DestroyableObject`` to ``ObjectTemplate.create SimpleObject``.

#. **Configure the .tweak file**: Open the new :file:`_nondest.tweak` file.

   - Remove all components and settings related to the destruction of the object (e.g., the ``Armor`` and ``StrategicObject`` components).
   - Delete the lines ``ObjectTemplate.isDestructable 1`` and ``ObjectTemplate.setNetworkableInfo BasicInfo``.
   - Update the template name to reference the non-destroyable object, while ensuring the geometry and collision mesh lines continue to reference the original destroyable static object.
   - Change ``ObjectTemplate.activeSafe DestroyableObject`` to ``ObjectTemplate.activeSafe SimpleObject``.

#. **Finalize**: Save all changes and close the files.
