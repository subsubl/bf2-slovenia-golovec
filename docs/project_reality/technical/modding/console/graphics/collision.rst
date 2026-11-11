
collisionManager
================

.. object:: CollisionCheck.checkStaticCollisionMeshes <int>

   :returns: void

.. object:: collisionManager.buildDebugCollisionMeshes

   :returns: void

.. object:: collisionManager.create <std::string>

   :returns: void

.. object:: collisionManager.createTemplate <std::string>

   :returns: void

   :Description: Creates a Collision Mesh template from the collision mesh name so it can be used in other files without creating a duplicate mesh
   :Used in: :file:`.con` files for collision meshes

.. object:: collisionManager.drawBoundingBoxes <bool>

   :returns: void

.. object:: collisionManager.drawForces <bool>

   :returns: void

.. object:: collisionManager.drawIntersectFaces <bool>

   :returns: void

.. object:: collisionManager.drawMeshes <bool>

   :returns: void

.. object:: collisionManager.drawNormals <bool>

   :returns: void

.. object:: collisionManager.drawOnlyRoot <float>

   :returns: void

.. object:: collisionManager.drawPivots <bool>

   :returns: void

.. object:: collisionManager.drawPrimitives <bool>

   :returns: void

.. object:: collisionManager.drawSoldierMesh <bool>

   :returns: void

.. object:: collisionManager.drawTestedFaces <bool>

   :returns: void

.. object:: collisionManager.getNameOfObjectInFocus

   :returns: void

.. object:: collisionManager.identityRotateObjectInFocus

   :returns: void

.. object:: collisionManager.rotateObjectInFocusAroundAxis <uint float>

   :returns: void

.. object:: collisionManager.rotateObjectInFocusAroundVector <Vec3 float>

   :returns: void

.. object:: collisionManager.setActiveLod <int>

   :returns: void

.. object:: collisionManager.setDrawDistance <float>

   :returns: void

.. object:: collisionManager.setGeometry <bool>

   :returns: void

.. object:: collisionManager.setSleepinessOfObjectInFocus <int>

   :returns: void

   - :file:`.con` presumably
   - Effect Unknown. Causes a game crash during loading when using ``collisionManager.setSleepinessOfObjectInFocus 0`` in a :file:`.con` of a ``GenericFirearm``

.. object:: collisionManager.updateFlagsOfObjectInFocus <U32 U32>

   :returns: void

.. object:: collisionManager.useDeferredLoading <bool>

   :returns: bool
