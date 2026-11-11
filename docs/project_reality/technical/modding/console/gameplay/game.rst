
Game
====

game
----

.. object:: game.allowToggleFullscreen <bool>

   :returns: bool

.. object:: game.lockFps <int>

   :returns: int

   Sets a fps cap, makes it so that the fps can't go higher than the given number.

.. object:: game.radioMessage <TargetChannel std::string>

   :returns: void

.. object:: game.sayAll <std::string>

   :returns: void

.. object:: game.sayTeam <int std::string>

   :returns: void

.. object:: game.simulationRate <int>

   :returns: int

   - :file:`HudElementsDemoRecComm.con`
   - In Battlerecorder it sets the speed for the decrease speed and increase speed buttons.
   - Can be increased, though some users report no difference as it is dependent on the Demo FPS (Default is 30 settings must be recorded higher something like 60) and Game FPS

.. object:: game.toggleFullscreen

   :returns: void

   - ~ Console
   - Toggles Full-Screen and Windowed mode
   - It will give you the nasty side-effect of seethrough terrain that would need the client to disconnect and reconnect to fix.

.. object:: game.unload

   :returns: bool

gameLogic
---------

.. object:: gameLogic.AddInvalidDropVehicleObject <std::string bool>

   :returns: void

.. object:: gameLogic.becomeSquadLeader <bool>

   :returns: bool

.. object:: gameLogic.createObject <std::string>

   :returns: void

.. object:: gameLogic.damageForBeingOutSideWorld <float>

   :returns: float

.. object:: gameLogic.defaultLevel <std::string>

   :returns: std::string

.. object:: gameLogic.defaultTimeToNextAIWave <float>

   :returns: float

.. object:: gameLogic.enableVoHelp <bool>

   :returns: bool

   - Enables the Voice Over Tips feature from vBF2.
   - Uses :file:`prhelp.utxt` in localization for std::strings/anything with HUD_HELP definitions
   - HudElementsHelp.con in Menu for the size, color, fade in time, create more messages and VoiceMessages_Help.con for voiceovers

.. object:: gameLogic.extraUAVVehicleFlightHeight <float>

   :returns: float

.. object:: gameLogic.feslEnvironment <int>

   :returns: int

.. object:: gameLogic.getBeforeSpawnCameraDirection

   :returns: Vec3

.. object:: gameLogic.getBeforeSpawnCameraPosition

   :returns: Vec3

.. object:: gameLogic.getDefaultNumberOfTickets <U32>

   :returns: U32

.. object:: gameLogic.getDefaultNumberOfTicketsEx <U32 U32>

   :returns: U32

.. object:: gameLogic.getNumberOfTickets <U32>

   :returns: U32

.. object:: gameLogic.getTeamDropVehicle <int>

   :returns: std::string

.. object:: gameLogic.getTeamLanguage <int>

   :returns: std::string

.. object:: gameLogic.getTeamName <int>

   :returns: std::string

.. object:: gameLogic.getTicketLossAtEndPerMin

   :returns: float

.. object:: gameLogic.getTicketLossPerMin <U32>

   :returns: float

.. object:: gameLogic.hitIndicationThreshold <float>

   :returns: float

.. object:: gameLogic.maximumLevelViewDistance <float>

   :returns: float

.. object:: gameLogic.messages.addHelpMessage <std::string std::string>

   :returns: int

.. object:: gameLogic.messages.addMessage <std::string>

   :returns: int

.. object:: gameLogic.messages.addRadioFilter <std::string std::string>

   :returns: int

.. object:: gameLogic.messages.addRadioVoice <std::string std::string std::string>

   :returns: int

.. object:: gameLogic.messages.playHelpMessage <std::string>

   :returns: int

.. object:: gameLogic.messages.playRadioMessage <int std::string std::string>

   :returns: int

.. object:: gameLogic.messages.setVolumes <float float>

   :returns: void

.. object:: gameLogic.noVehiclesOmit <std::string>

   :returns: void

.. object:: gameLogic.outputPlayerStats <bool>

   :returns: bool

.. object:: gameLogic.printCameraCoordToConsole

   :returns: void

.. object:: gameLogic.refreshTriggerables

   :returns: void

.. object:: gameLogic.remoteCommand <int int int>

   :returns: bool

.. object:: gameLogic.reset

   :returns: void

.. object:: gameLogic.roundNr <int>

   :returns: int

.. object:: gameLogic.setAirMouseInverted <bool>

   :returns: void

.. object:: gameLogic.setAirMouseSensitivity <float>

   :returns: float

.. object:: gameLogic.setBeforeSpawnCamera <Vec3 Vec3>

   :returns: void

.. object:: gameLogic.setDefaultNumberOfTickets <U32 U32>

   :returns: void

.. object:: gameLogic.setDefaultNumberOfTicketsEx <U32 U32 U32>

   :returns: void

.. object:: gameLogic.setDropVehicleDeviationRadius <int int>

   :returns: void

.. object:: gameLogic.setKit <int KitType std::string>

   :returns: void

.. object:: gameLogic.setNumberOfTickets <U32 U32>

   :returns: void

.. object:: gameLogic.setNumDropVehiclesForTeam <int int>

   :returns: void

.. object:: gameLogic.setTeamDropVehicle <int std::string>

   :returns: void

.. object:: gameLogic.setTeamFlag <int std::string>

   :returns: void

.. object:: gameLogic.setTeamLanguage <int std::string>

   :returns: void

.. object:: gameLogic.setTeamName <int std::string>

   :returns: void

.. object:: gameLogic.setTicketLossAtEndPerMin <float>

   :returns: void

.. object:: gameLogic.setTicketLossPerMin <U32 float>

   :returns: void

.. object:: gameLogic.spawnAtCameraPosition <bool>

   :returns: bool

.. object:: gameLogic.spawnObjectSpeed <float>

   :returns: float

.. object:: gameLogic.spawnPlayers <bool>

   :returns: bool

.. object:: gameLogic.supplyDropHeight <float>

   :returns: float

.. object:: gameLogic.supplyDropNumSecsToLive <float>

   :returns: float

.. object:: gameLogic.teleport

   :returns: void

.. object:: gameLogic.teleportCameraTo <Vec3>

   :returns: void

.. object:: gameLogic.teleportTo <Vec3>

   :returns: void

.. object:: gameLogic.timeAllowedOutSideWorld <float>

   :returns: float

.. object:: gameLogic.timeToNextAIWave <float>

   :returns: float

.. object:: gameLogic.togglePause

   :returns: void

   Console ~ Command

   Pauses the game. Pressing :kbd:`P` in COOP and Local does the same thing.

.. object:: gameLogic.vehicleDropHeight <float>

   :returns: float

gameServerSettings
------------------

.. object:: gameServerSettings.setAdminScript <std::string>

   :returns: void

.. object:: gameServerSettings.setAllowNATNegotation <bool>

   :returns: void

.. object:: gameServerSettings.setAutoBalanceTeam <bool>

   :returns: void

.. object:: gameServerSettings.setAutoRecord <bool>

   :returns: void

.. object:: gameServerSettings.setAutoRecordRounds <int>

   :returns: void

.. object:: gameServerSettings.setCommunityLogoURL <std::string>

   :returns: void

.. object:: gameServerSettings.setCoopBotCount <int>

   :returns: void

.. object:: gameServerSettings.setCoopBotDifficulty <float>

   :returns: void

.. object:: gameServerSettings.setCoopBotRatio <float>

   :returns: void

.. object:: gameServerSettings.setDemoDownloadURL <std::string>

   :returns: void

.. object:: gameServerSettings.setDemoHook <std::string>

   :returns: void

.. object:: gameServerSettings.setDemoIndexURL <std::string>

   :returns: void

.. object:: gameServerSettings.setEndDelay <int>

   :returns: void

.. object:: gameServerSettings.setFriendlyFireWithMines <bool>

   :returns: void

.. object:: gameServerSettings.setGameMode <std::string>

   :returns: void

.. object:: gameServerSettings.setGameSpyPort <int>

   :returns: void

.. object:: gameServerSettings.setInterfaceIP <std::string>

   :returns: void

.. object:: gameServerSettings.setInternet <bool>

   :returns: void

.. object:: gameServerSettings.setManDownTime <float>

   :returns: void

.. object:: gameServerSettings.setMaxPlayers <int>

   :returns: void

.. object:: gameServerSettings.setMinPlayersForVoting <int>

   :returns: void

.. object:: gameServerSettings.setNoVehicles <float>

   :returns: void

.. object:: gameServerSettings.setPassword <std::string>

   :returns: void

.. object:: gameServerSettings.setPunishTeamKills <bool>

   :returns: void

.. object:: gameServerSettings.setRoundsPerMap <int>

   :returns: void

.. object:: gameServerSettings.setScoreLimit <int>

   :returns: void

.. object:: gameServerSettings.setServerName <std::string>

   :returns: void

.. object:: gameServerSettings.setSoldierFF <int>

   :returns: void

.. object:: gameServerSettings.setSoldierSplashFF <int>

   :returns: void

.. object:: gameServerSettings.setSpawnTime <float>

   :returns: void

.. object:: gameServerSettings.setSponsorLogoURL <std::string>

   :returns: void

.. object:: gameServerSettings.setSponsorText <std::string>

   :returns: void

.. object:: gameServerSettings.setStartDelay <int>

   :returns: void

.. object:: gameServerSettings.setSvPunkBuster <bool>

   :returns: void

.. object:: gameServerSettings.setTeamRatio <float>

   :returns: void

.. object:: gameServerSettings.setTeamVoteOnly <bool>

   :returns: void

.. object:: gameServerSettings.setTicketRatio <int>

   :returns: void

.. object:: gameServerSettings.setTimeBeforeRestartMap <float>

   :returns: void

.. object:: gameServerSettings.setTimeLimit <int>

   :returns: void

.. object:: gameServerSettings.setVehicleFF <int>

   :returns: void

.. object:: gameServerSettings.setVehicleSplashFF <int>

   :returns: void

.. object:: gameServerSettings.setVoipBFClientPort <int>

   :returns: void

.. object:: gameServerSettings.setVoipBFServerPort <int>

   :returns: void

.. object:: gameServerSettings.setVoipEnabled <bool>

   :returns: void

.. object:: gameServerSettings.setVoipQuality <int>

   :returns: void

.. object:: gameServerSettings.setVoipServerPort <int>

   :returns: void

.. object:: gameServerSettings.setVoipServerRemote <bool>

   :returns: void

.. object:: gameServerSettings.setVoipServerRemoteIP <std::string>

   :returns: void

.. object:: gameServerSettings.setVoipSharedPassword <std::string>

   :returns: void

.. object:: gameServerSettings.setVoteTime <int>

   :returns: void
