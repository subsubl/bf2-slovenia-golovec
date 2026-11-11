
BF2 Engine Internals
====================

The BF2 engine is written in C++ and uses the Standard Template Library (STL) extensively.

.. important::

   All virtual functions on this page are in the order they are defined in the vtable unless otherwise specified.

Reference Counting
------------------

Many internal game components use intrusive reference counting via inheritance. The base class is similar to this:

.. code-block:: cpp

   class RefCounted
   {
   public:
      RefCounted() : m_refCount(1) {}

      virtual int addRef() {
         return ++m_refCount;
      }

      virtual int getRefCount() const {
         return m_refCount;
      }

      // Unsure if there actually is a base implementation of this method,
      // this sometimes points to a unique function in the vtable but follows this pattern.
      virtual int release() {
         if (--m_refCount == 0) {
            delete (RefCounted*)this;
         }
         return m_refCount;
      }

      // Position of the destructor in the vtable may change.
      virtual ~RefCounted() {}
   private:
      int m_refCount;
   };

.. note::

   This class is not thread-safe, mirroring the actual implementation.

ClassManager
------------

The program has one ClassManager instance. It dynamically accesses different game subsystems. These subsystems are registered with a string identifier (class name), an instance pointer, a class ID, and another unknown integer. They can then be accessed by their class name. The following classes are registered in BF2.exe:

- ``GameServerSettings``
- ``HudInformationLayer``
- ``DistributedLightRenderer``
- ``LocalProfileManager``
- ``ProfileManager``
- ``RankManager``
- ``ClanManager``
- ``NewsManager``
- ``AutoPatch``
- ``Persistence``
- ``MenuTeamManager``
- ``GlobalSettings``
- ``VideoSettings``
- ``AudioSettings``
- ``ControlSettings``
- ``GeneralSettings``
- ``HapticSettings``
- ``ServerBrowserManager``
- ``SwiffHost``
- ``DemoLibrary``
- ``ServerLogoManager``
- ``ModInfo``

The rendering module (RendDX9.dll) also registers these classes:

- ``SwiffRenderer``
- ``Terrain``
- ``LightManager``
- ``GeometryTemplateManager``
- ``StaticMeshRenderer``
- ``SkinnedMeshRenderer``
- ``ParticleSystemManager``
- ``HemiMapManager``
- ``DecalManager``
- ``DecalShadowManager``
- ``RoadCompiledRenderer``
- ``RoadEditableRenderer``
- ``NametagManager``
- ``SkyDome``
- ``UndergrowthSystem``
- ``LightingManager``
- ``WeatherManager``
- ``RainManager``
- ``RenderView``
- ``EnvMapManager``

Common
------

GameEvent
^^^^^^^^^

The game uses multiple event systems. Game events are in-game occurrences related to gameplay.

.. code-block:: cpp
   :caption: The incomplete class below is the base for all events, which often include extra data. A GameEvent has a maximum size of 1024 bits, defined by ``const uint MaximumGameEventSize``.

   class GameEvent : public RefCounted
   {
   public:
      GameEvent() : field_8(-1) {}

      // multiple virtual functions here
   private:
      int field_8;
   };

List of Game events:

- ``ChallengeEvent``
- ``ChallengeResponseEvent``
- ``ConnectionTypeEvent``
- ``DataBlockEvent``
- ``CreatePlayerEvent``
- ``CreateObjectEvent``
- ``CreateKitEvent``
- ``DestroyObjectEvent``
- ``DestroyPlayerEvent``
- ``EnterVehicleEvent``
- ``ExitVehicleEvent``
- ``PostRemoteEvent``
- ``ChangePlayerNameEvent``
- ``HandlePickupEvent``
- ``HandleDropEvent``
- ``StringBlockEvent``
- ``JoinSquadEvent``
- ``LeaveSquadEvent``
- ``CommanderEvent``
- ``RadioMessageEvent``
- ``KilledByEvent``
- ``ChangeSquadNameEvent``
- ``SetPrivateSquadEvent``
- ``IssueSquadOrderEvent``
- ``InviteEvent``
- ``RankEvent``
- ``KickBanEvent``
- ``SetAcceptOrderEvent``
- ``SetSquadLeaderEvent``
- ``SpottedEvent``
- ``ArtilleryEvent``
- ``StickyProjectileEvent``
- ``AmbientEffectAreaEvent``
- ``VoipOnOffEvent``
- ``CommanderCamEvent``
- ``SupplyDropEvent``
- ``VoidPlayerMuteEvent``
- ``VoteEvent``
- ``TargetDirectionEvent``
- ``BeginRoundEvent``
- ``EndOfRoundEvent``
- ``PythonCommandEvent``
- ``RequestEvent``
- ``VoipSessionEvent``
- ``ToggleFreeCameraEvent``
- ``MedalEvent``
- ``UnlockEvent``
- ``MissileInitEvent``
- ``UAVEvent``
- ``ContentCheckEvent``
- ``DropVehicleEvent``
- ``CreateSpawnGroupEvent``
- ``RemoveSpawnGroupEvent``
- ``UpdateTriggerEvent``
- ``GrapplingHookContainerCreateEvent``
- ``GrapplingHookContainerUpdateEvent``
- ``GrapplingHookContainerDetachEvent``
- ``GrapplingHookCreateEvent``
- ``GrapplingHookUpdateEvent``
- ``PlayerTearGassedEvent``
- ``SetNightVisionEvent``
- ``VerifyPlayerTeamEvent``
- ``FixPlayerTeamEvent``

IO
--

The FileManager, accessed via the ClassManager, handles filesystem access.

Stream
^^^^^^

.. code-block:: cpp
   :caption: This interface is used by FileManager for file operations.

   class Stream
   {
   public:
      virtual unsigned read(void* buffer, unsigned numBytes) = 0;
      virtual bool write(void* buffer, unsigned numBytes) = 0;
      virtual int unk_1() {};
      virtual int unk_2() {};
      virtual Stream clone() = 0;
      virtual int unk_3() {};
      virtual int unk_4() {};
      virtual int unk_5() {};
      virtual bool seek(unsigned moveMethod, long distanceToMove) = 0;
      virtual unsigned getPosition() = 0;
      virtual unsigned getSize() = 0;
   };

FileSystem
^^^^^^^^^^

.. code-block:: cpp
   :caption: This interface is used and implemented by the FileManager to access the file system.

   class FileSystem
   {
   public:
      virtual int unk_1() {}
      virtual int unk_2() {}
      virtual Stream* openFile(std::string* path) = 0;
      virtual int unk_3() {}
      virtual int unk_4() {}
      virtual int unk_5() {}
      virtual int unk_6() {}
      virtual bool readFile(std::string* path, void* buffer, unsigned numBytes, unsigned* bytesRed) = 0;
      virtual int unk_7() {}
      virtual int findFiles(std::string* folderPath, ? a, ? b) = 0;
      virtual int getFileInfo(std::string* path, ? a) = 0;
      virtual int compareFileTime(std::string* path, std::string* otherPath) = 0;
      virtual bool getFullFileName(std::string* path) = 0;
      virtual void update() = 0;
   };
