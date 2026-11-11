
Animation
=========

AnimationBundle
---------------

.. object:: animationBundle.abruptPlayback <bool>

   :returns: bool

.. object:: animationBundle.addAnimation <std::string>

   :returns: void

.. object:: animationBundle.addEvent <std::string>

   :returns: void

.. object:: animationBundle.fadeInTime <float>

   :returns: float

   :Used in: AnimationSystem1p and 3p :file:`.inc` files
   :Fade-in: Animation Start. Allows a smooth transition between animations.

   - The lower it is, the quicker it is.
   - A high value makes the transition slower and longer.
   - Fade in 0.01.

   :Example: Idle/Walking to Sprinting

.. object:: animationBundle.fadeOutTime <float>

   :returns: float

   :Used in: AnimationSystem1p and 3p :file:`.inc` files
   :Fade out: Animation End.

   - Same as above, Fadeout ``0.1``.
   - Fadeout ``0.4`` would make it take ``0.4`` seconds to finish an animation

   :Example: From Sprinting to Walk/Idle

.. object:: animationBundle.getAnimationLength <std::string>

   :returns: float

.. object:: animationBundle.getAnimationStartTime <std::string>

   :returns: float

.. object:: animationBundle.getEventStartTime <std::string>

   :returns: float

.. object:: animationBundle.isLooping <bool>

   :returns: bool

.. object:: animationBundle.jumpToLastAnimationAtStop <bool>

   :returns: bool

.. object:: animationBundle.length <float>

   :returns: float

.. object:: animationBundle.listAnimations

   :returns: std::string

.. object:: animationBundle.listEvents

   :returns: std::string

.. object:: animationBundle.playBackward <bool>

   :returns: bool

.. object:: animationBundle.playForever <bool>

   :returns: bool

.. object:: animationBundle.removeAnimation <std::string>

   :returns: void

.. object:: animationBundle.removeEvent <std::string>

   :returns: void

.. object:: animationBundle.setAnimationLength <std::string float>

   :returns: void

.. object:: animationBundle.setAnimationStartTime <std::string float>

   :returns: void

.. object:: animationBundle.setEventStartTime <std::string float>

   :returns: void

.. object:: animationBundle.useSpeedAsTime <bool>

   :returns: bool

AnimationManager
----------------

.. object:: animationManager.fadeInTime <float>

   :returns: float

.. object:: animationManager.ignoreMotherOrientation <int>

   :returns: int

.. object:: animationManager.length <float>

   :returns: float

   :Description: The length of the animation. Must match up with ``ObjectTemplate.ammo.reloadTime`` to sync.
   :Used in: "AnimationSystem1p, AnimationSystem3p.inc"
   :Lower value: Animation will be sped up.
   :Higher value: Animation will be slowed down.

.. object:: animationManager.looping <bool>

   :returns: bool

   :Used in: "AnimationSystem1p, AnimationSystem3p.inc"

.. object:: animationManager.noiceAmplitude <float>

   :returns: float

.. object:: animationManager.noiceFreq <int>

   :returns: int

.. object:: animationManager.originalLength

   :returns: float

AnimationSystem
---------------

.. object:: animationSystem.activestd::string

   :returns: std::string

.. object:: animationSystem.activeAnimation <std::string>

   :returns: std::string

.. object:: animationSystem.activeBundle <std::string>

   :returns: std::string

.. object:: animationSystem.activeTrigger <std::string>

   :returns: std::string

.. object:: animationSystem.activeValueHolder <std::string>

   :returns: std::string

.. object:: animationSystem.cameraSpring.amplitude <Vec3>

   :returns: Vec3

.. object:: animationSystem.cameraSpring.fire <Vec3>

   :returns: Vec3

.. object:: animationSystem.cameraSpring.hit <Vec3>

   :returns: Vec3

.. object:: animationSystem.cameraSpring.look <Vec2>

   :returns: Vec2

.. object:: animationSystem.cameraSpring.move <Vec3>

   :returns: Vec3

.. object:: animationSystem.cameraSpring.stiffness <Vec3>

   :returns: Vec3

.. object:: animationSystem.cameraSpring.use <bool>

   :returns: bool

.. object:: animationSystem.cameraSpring.zoomDamping <Vec3>

   :returns: Vec3

.. object:: animationSystem.create <std::string>

   :returns: void

.. object:: animationSystem.createAnimation <std::string>

   :returns: anim.BoneAnimation\*

.. object:: animationSystem.createBundle <std::string>

   :returns: anim.Bundle\*

.. object:: animationSystem.createTrigger <std::string std::string>

   :returns: anim.Trigger\*

.. object:: animationSystem.createValueHolder <std::string>

   :returns: void

.. object:: animationSystem.deleteActiveBundle

   :returns: void

.. object:: animationSystem.deleteActiveTrigger

   :returns: void

.. object:: animationSystem.hide

   :returns: void

.. object:: animationSystem.list

   :returns: std::string

.. object:: animationSystem.listAnimations

   :returns: std::string

.. object:: animationSystem.listBundles

   :returns: std::string

.. object:: animationSystem.listTriggers

   :returns: std::string

.. object:: AnimationSystem.listTriggerTypes

   :returns: std::string

.. object:: animationSystem.listValueHolders

   :returns: std::string

.. object:: animationSystem.playbackModifier <float>

   :returns: float

.. object:: animationSystem.reloadScript

   :returns: void

.. object:: animationSystem.save <std::string>

   :returns: void

.. object:: animationSystem.saveActive

   :returns: void

.. object:: animationSystem.saveValueHolders

   :returns: void

animationTrigger
----------------

.. object:: animationTrigger.addBundle <std::string>

   :returns: void

.. object:: animationTrigger.addChild <std::string>

   :returns: void

.. object:: animationTrigger.clearValueHolder

   :returns: void

.. object:: animationTrigger.fadeInTime <float>

   :returns: float

.. object:: animationTrigger.getTypeName

   :returns: std::string

.. object:: animationTrigger.idleTime <Vec2>

   :returns: Vec2

.. object:: animationTrigger.listBundles

   :returns: std::string

.. object:: animationTrigger.message <int>

   :returns: int

.. object:: animationTrigger.removeBundle <std::string>

   :returns: void

.. object:: animationTrigger.removeChild <std::string>

   :returns: void

.. object:: animationTrigger.triggerOnAcceleration <bool>

   :returns: bool

.. object:: animationTrigger.useDirection <bool>

   :returns: bool

.. object:: animationTrigger.valueHolder <std::string>

   :returns: std::string

animationValueHolder
--------------------

.. object:: animationValueHolder.getFilename

   :returns: std::string

.. object:: animationValueHolder.max <float>

   :returns: float

.. object:: animationValueHolder.min <float>

   :returns: float

.. object:: animationValueHolder.normal <float>

   :returns: float

.. object:: animationValueHolder.passOnMessage <unsigned int>

   :returns: unsigned int

.. object:: animationValueHolder.stopOnMessage <unsigned int>

   :returns: unsigned int

.. object:: animationValueHolder.values <float float float>

   :returns: void
