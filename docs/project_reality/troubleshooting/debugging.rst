
Running The Debugger
====================

The BF2/PR debugger is very useful for finding bugs that don't show error messages. However, you need to know how to read the log messages it produces.

#. Download these files, which have been changed to work with the debugger (they are older than the current release, but this doesn't affect their function):

   :download:`Debugger Files <https://files.realitymod.com/resources/Debugger_files.zip>`

   :download:`Menu Files <https://drive.google.com/file/d/1ZWQdh90h0eTIO9okBuOxm7SRyMxavCNS/view?usp=sharing>`

#. Extract the Debugger files into your main Project Reality folder (for example, :file:`C:\\Program Files (x86)\\Project Reality\\Project Reality BF2\\`). Extract the modified menu files into ``mods/pr_edit/content``.

   Make sure to do this AFTER you have finished step 4 of the editor setup tutorial.

#. Start the regular PR launcher.

   :menuselection:`Right-click PLAY --> Launch Debugger`

#. Next, you need to create a profile that will work correctly with the debugger.

   :menuselection:`Manage Profiles --> Create a New Offline Profile`

#. Change this profile into a debugger profile.

   :menuselection:`Your profile --> Convert Profile`

#. Depending on what you want to do, you might want to go back to the :guilabel:`Options` menu in the launcher. Select the debugger profile to reduce the resolution and turn off fullscreen mode. This is because fullscreen mode only creates logs, while windowed mode also displays error windows for more critical errors.

#. Return to the debugger screen: :menuselection:`Right-click PLAY --> Launch debugger --> Select your new profile --> log in`

.. note::

   When you use the debugger in windowed mode, you will see error messages frequently appear during loading. These are usually about texture coordinates and can be ignored. Just click Continue to close them all.

Log messages are saved in :file:`mods/pr/logs`.

   You will find two types of log messages: a BFLog and a Debug log. The Debug log contains many details about what the system is currently doing. The BFLog is more like the standard error messages you might see, focusing on errors rather than general notifications.

.. note::

   Typically, any errors and crashes will be the last entries in the log, but this is not always the case. We have found that errors related to collision meshes, and sometimes other issues, may not appear at the very end. Therefore, you should review the Debug log for "Error" or "Warning" messages (you'll notice entries starting with Debug, Warning, Error, Assert, etc.). Check if these messages relate to anything you have recently changed. This is usually where you'll find the problem. Good luck! If you encounter any difficulties, please visit the community modding forums and create a post about your issue.
