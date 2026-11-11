
BF2 Timer & Logger
==================

This module provides enhanced timer functionalities and a robust logging system for Project Reality.

BF2 Timer
---------

The Project Reality timer (:py:mod:`realitytimer`) enhances the default timer interface with the following features:

- **Exception Handling**: Includes exception catching with debug messages for unhandled exceptions, preventing server crashes due to faulty code.
- **Internal Safety Check**: Ensures timers do not fire after :py:meth:`Timer.destroy` has been called, which can occur when :py:meth:`Timer.destroy` is invoked on the same tick.

.. py:module:: realitytimer

   .. py:class:: Timer(object)

      A timer class that triggers a target function after a specified delay or at recurring intervals.

      .. py:method:: __init__(targetFunc, delta, alwaysTrigger, data=None)

         Initializes a new Timer instance.

         :param targetFunc: The function to be called when the timer triggers.
         :type targetFunc: function
         :param delta: The delay in seconds before the timer first triggers.
         :type delta: float
         :param alwaysTrigger: If ``1`` the timer will always trigger even if the game is paused or in a state where it normally wouldn't.
         :type alwaysTrigger: int
         :param data: Optional data to be passed to the target function when it is called.
         :type data: any, optional

         The timer's internal time is set based on the current wall clock time plus the delta. It also registers the timer with the host.

      .. py:method:: destroy()

         Destroys the timer, marking it as inactive and notifying the host.

         This method prevents the timer from triggering further and cleans up associated resources.
         It includes a check to ensure it's only called once.

      .. py:method:: getTime()

         Retrieves the current set time for the timer.

         :return: The current time value of the timer.
         :rtype: float

      .. py:method:: setTime(time)

         Sets the timer's current time to a new value.

         :param time: The new time value to set for the timer.
         :type time: float

      .. py:method:: setRecurring(interval)

         Configures the timer to be recurring.

         :param interval: The interval in seconds at which the timer should re-trigger after the initial trigger. A value of 0.0 means it is not recurring.
         :type interval: float

      .. py:method:: onTrigger()

         This method is called when the timer is due to trigger. It executes the ``targetFunc`` with the associated data.
         It includes optional profiler debugging to log execution time and handles exceptions gracefully.
         If the timer has been destroyed, it will not execute the target function.

   .. py:class:: fireOnce(Timer)

      A utility class for firing a function once after a specified delay without needing to store a timer reference. It inherits from :py:class:`Timer` and destroys itself after firing.

      .. py:method:: __init__(targetFunc, delay, data=None)

         Initializes a ``fireOnce`` timer.

         :param targetFunc: The function to be called after the specified delay.
         :type targetFunc: function
         :param delay: The delay in seconds before the function is called.
         :type delay: float
         :param data: Optional data to pass to the ``targetFunc``.
         :type data: any, optional

         This timer is added to the ``activeFireOnceTimers`` set.

      .. py:method:: onTrigger()

         Calls the parent ``onTrigger`` and then destroys the timer.

      .. py:method:: destroy()

         Destroys the timer and removes it from the ``activeFireOnceTimers`` set.

      .. py:method:: setRecurring(interval)

         Raises an exception as this functionality is not supported for :py:class:`fireOnce` timers.

      .. py:method:: setTime(time)

         Raises an exception as this functionality is not supported for :py:class:`fireOnce` timers.

   .. py:class:: fireNextTick(fireOnce)

      A specialized timer that fires the target function on the next game tick. It inherits from :py:class:`fireOnce` and uses a delay of -1 to achieve this behavior.

      .. py:method:: __init__(targetFunc, data=None)

         Initializes a ``fireNextTick`` timer.

         :param targetFunc: The function to be called on the next game tick.
         :type targetFunc: function
         :param data: Optional data to pass to the ``targetFunc``.
         :type data: any, optional

   .. py:class:: coolDown

      A class for maintaining a "cooldown" system for functions.

      .. py:method:: __init__(targetFunc, args=None)

         Initializes the cooldown system.

         :param targetFunc: The function to be called after the cooldown period.
         :type targetFunc: function
         :param args: Optional arguments to pass to the target function.
         :type args: any, optional

         The cooldown timer is initially set to None.

      .. py:method:: reset()

         Resets the cooldown. If a timer is active, it is destroyed.

      .. py:method:: start(time)

         Starts the cooldown period.

         :param time: The duration of the cooldown in seconds. If set to ``None`` the cooldown is permanently disabled.
         :type time: float or None

         If ``time`` is ``None`` the cooldown is effectively disabled forever by setting ``self._timer`` to ``False``. Otherwise, a :py:class:`fireOnce` timer is created.

      .. py:method:: isOnCoolDown()

         Checks if the cooldown is currently active (i.e., a timer is running and not disabled forever).

         :return: True if a cooldown timer is active, False otherwise.
         :rtype: bool

      .. py:method:: isOnCoolDownForever()

         Checks if the cooldown is set to be permanently disabled.

         :return: True if the cooldown is disabled forever, False otherwise.
         :rtype: bool

      .. py:method:: getTimeLeft()

         Returns the time remaining in the cooldown period.

         :return: The time left in seconds. Returns -1.0 if disabled forever, 0.0 if not on cooldown, and the remaining time otherwise.
         :rtype: float

   .. py:class:: repeatingTask

      Represents a task that is scheduled to run repeatedly at a specified interval. It uses a min-heap to manage execution order.

      .. py:method:: __init__(targetFunc, interval, data=None)

         Initializes a repeating task.

         :param targetFunc: The function to execute when the task triggers.
         :type targetFunc: function
         :param interval: The time interval in seconds between task executions.
         :type interval: float
         :param data: Optional data to pass to the target function.
         :type data: any, optional

         The task's next execution time is calculated based on the current time plus the interval. It's then added to the ``_taskManager``'s task queue.

      .. py:method:: destroy()

         Marks the task for destruction, so it will not be executed again.

      .. py:method:: onTrigger()

         Executes the task's target function if the game state is 'Playing'.
         Includes optional profiling to measure execution time and logs errors if they occur.

   .. py:class:: task(repeatingTask)

      A specialized repeating task that is executed only once. It inherits from :py:class:`repeatingTask` and marks itself as destroyed after its ``onTrigger`` method is called.

      .. py:method:: onTrigger()

         Overrides the parent ``onTrigger`` to mark the task as destroyed after execution.

   .. py:function:: init()

      Initializes the timer system and registers necessary handlers.

      It registers a handler for game status changes to clean up timers on round end.
      A recurring timer :py:class:`Timer` (``perTickRefresh, 0.1, 1``) is created to periodically call ``perTickRefresh``.
      The ``_taskManager.refresh`` method is registered to be called on every tick.

   .. py:function:: cleanupOnRoundEnd(status)

      Handles cleanup actions when the game round ends.

      :param status: The current game status (e.g., :py:attr:`bf2.GameStatus.EndGame`).
      :type status: bf2.GameStatus

      If the game status is :py:attr:`bf2.GameStatus.EndGame` it iterates through all active :py:class:`fireOnce` timers and destroys them.

   .. py:class:: _taskManager

      Manages a queue of :py:class:`repeatingTask` objects, ensuring that tasks are executed efficiently and do not cause long ticks by spreading their execution over time.

      .. py:classmethod:: refresh(data=None)

         Refreshes the task queue by removing destroyed tasks and executing tasks that are due.

         It processes tasks from the ``taskQueue`` as long as they are due and the total execution time for this refresh cycle is within a small limit (e.g., 2ms) to prevent blocking the game loop. Tasks are re-added to the queue if they are not destroyed and have a recurring interval.
         Any tasks that have ``isDestroyed`` set to True are removed from the queue.

Reality Logger
--------------

The :py:mod:`realitylogger` module provides a flexible system for creating and managing log files within the game.

.. py:module:: realitylogger

   .. py:function:: createLogger(name, path, fileName, continous)

      Creates or retrieves a logger instance.

      :param name: A unique key used to identify and select the logger.
      :type name: str
      :param path: The directory where the log file will be created.
      :type path: str
      :param fileName: The name of the file to be created. If ``continous`` is False, this should specify a date format (strftime format).
      :type fileName: str
      :param continous: Determines whether logging occurs in a single file continuously or if a new file is created for each round.
      :type continous: bool

      This function can be called multiple times with the same key; repeated calls will be properly filtered. It is not necessary to place this call within an :py:func:`init` function.

   .. py:function:: removeLogger(name)

      Removes a logger instance associated with the given name.

      :param name: The unique key identifying the logger to remove.
      :type name: str

Using a logger
^^^^^^^^^^^^^^

To use the logger, you first need to acquire an instance using its key.

.. code-block:: python

   # Aquire a logger
   X = realitylogger.RealityLogger[key]

   # Basic logging commands
   X.logLine(line)
   X.logLines(lines)

   # You can also check if a logger exists
   if key in realitylogger.RealityLogger:
       pass

   # And get the number of active loggers
   num_loggers = len(realitylogger.RealityLogger)

Internal logger management is handled by the :py:class:`_RealityLogger` class, which manages logger instances and their lifecycle, including reacting to game status changes.

.. py:class:: _RealityLogger

   Manages a collection of logger instances.

   .. py:method:: onGameStatusChanged(self, status)

      Handles game status changes. If the game status is :py:attr:`bf2.GameStatus.Loading` and it's not the very first load, it reopens the stream for any non-continuous loggers.

      :param status: The current game status.
      :type status: bf2.GameStatus

   .. py:method:: createLogger(self, name, path, fileName, continous)

      Adds a new logger instance to the manager. See :py:func:`realitylogger.createLogger` for parameter details.

   .. py:method:: removeLogger(self, name)

      Removes a logger instance from the manager.

      :param name: The name of the logger to remove.
      :type name: str

Reality Server
--------------

.. py:module:: realityserver

   This module contains core server logic and management functions for Project Reality.

   .. py:function:: init()

      Initializes the server by verifying settings, checking for shutdown locks, and registering necessary handlers for game status changes (``onGameStatusChanged``), round starts (``onRoundStart``), and remote commands. It also sets the server name and properties.

   .. py:function:: getPlayerHash(player)

      Retrieves a unique hash for the specified player.

      :param player: The player object for whom to retrieve the hash.
      :type player: PlayerObject (assumed)
      :return: A unique hash string representing the player.
      :rtype: str

   .. py:function:: onGameStatusChanged(status)

      Handles various game status changes. It manages configuration loading and server property setup upon game ``Loaded`` status, including mod detection. For ``EndGame`` status, it restores server configuration.

      :param status: The current game status (e.g., :py:attr:`bf2.GameStatus.Loaded` :py:attr:`bf2.GameStatus.EndGame`).
      :type status: bf2.GameStatus

   .. py:function:: setServerProperties(properties=None)

      Applies server properties, either default or specified, to the running server instance using RCON commands. This function is crucial for configuring various game settings like man down time, spawn time, and timelimit.

   .. py:function:: isInternetServer()

      :return: ``True`` if the server is configured as an internet server.
      :rtype: bool

   .. py:function:: isPasswordedServer()

      :return: ``True`` if the server is password-protected.
      :rtype: bool

   .. py:function:: isCoopServer()

      :return: ``True`` if the server is running in cooperative mode.
      :rtype: bool
