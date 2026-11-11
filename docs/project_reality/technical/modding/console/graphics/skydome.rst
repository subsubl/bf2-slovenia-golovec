
skyDome
=======

.. object:: skyDome.cloudLerpFactors <Vec2>

   :returns: Vec2

.. object:: skyDome.cloudTemplate <std::string>

   :returns: std::string

.. object:: skyDome.cloudTexture <std::string>

   :returns: std::string

.. object:: skyDome.cloudTexture2 <std::string>

   :returns: std::string

.. object:: skyDome.domePosition <Vec3>

   :returns: Vec3

.. object:: skyDome.domeRotation <float>

   :returns: float

.. object:: skyDome.domeSize <float>

   :returns: float

.. object:: skyDome.fadeCloudsDistances <Vec2>

   :returns: Vec2

.. object:: skyDome.flareDirection <Vec3>

   :returns: Vec3

.. object:: skyDome.flareFadeAdd <float>

   :returns: float

.. object:: skyDome.flareFadeMul <float>

   :returns: float

.. object:: skyDome.flareTemplate <std::string>

   :returns: std::string

.. object:: skyDome.flareTexture <std::string>

   :returns: std::string

   - Map: :file:`Sky.con`
   - The texture of the sunflare/actual sunflare.
   - When switching to a map with no sunflare, it will still use the previous maps one.

     - So for maps like Fallujah West/Saaremaa, an invisible texture needs to be defined instead to prevent the sunflare bug.

   - Usage: ``Skydome.flareTexture common\textures\sunflare\Sunglow_no``

.. object:: skyDome.hasCloudLayer <bool>

   :returns: bool

.. object:: skyDome.hasCloudLayer2 <bool>

   :returns: bool

.. object:: skyDome.lightingBlend <float>

   :returns: float

.. object:: skyDome.lightingColor <Vec3>

   :returns: Vec3

.. object:: skyDome.scrollDirection <Vec2>

   :returns: Vec2

.. object:: skyDome.scrollDirection2 <Vec2>

   :returns: Vec2

.. object:: skyDome.skyTemplate <std::string>

   :returns: std::string

.. object:: skyDome.skyTexture <std::string>

   :returns: std::string
