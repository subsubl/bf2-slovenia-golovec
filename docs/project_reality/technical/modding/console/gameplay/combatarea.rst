
combatArea
==========

.. object:: combatArea.active <std::string>

   :returns: void

.. object:: combatArea.addAreaPoint <Vec2>

   :returns: void

.. object:: combatArea.create <std::string>

   :returns: void

.. object:: combatArea.deleteActiveCombatArea

   :returns: void

.. object:: combatArea.getActiveCombatAreaName

   :returns: std::string

.. object:: combatArea.inverted <bool>

   :returns: bool

.. object:: combatArea.layer <int>

   :returns: int

.. object:: combatAreaManager.addVehicleDamage <world::VehicleCategory float>

   :returns: void

.. object:: combatAreaManager.addVehicleTimer <world::VehicleCategory float>

   :returns: void

.. object:: combatAreaManager.damage <float>

   :returns: float

.. object:: combatAreaManager.timeAllowedOutside <float>

   :returns: float

.. object:: combatAreaManager.use <bool>

   :returns: void

.. object:: combatArea.max <Vec2>

   :returns: Vec2

.. object:: combatArea.min <Vec2>

   :returns: Vec2

.. object:: combatArea.team <int>

   :returns: int

.. object:: combatArea.usedByPathFinding <bool>

   :returns: bool

.. object:: combatArea.vehicles <int>

   :returns: int

   Controls what kind of vehicle is effected by the combat zone. This can be used for crating an extra large, separate combat zone around the base combat zone only for jets, to give them a much larger area to fly in and when you hop into a jet, you can still see the base combat zone, but the area between the base and the jet combat zone will be 1/2 transparent. When hand coding this, the values are:

   :VehicleType 0: Land
   :VehicleType 1: Sea
   :VehicleType 2: Planes
   :VehicleType 3: Choppers
   :VehicleType 4: All
   :VehicleType 5: Planes & Choppers
