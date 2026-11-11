
HudEvent
========

This section provides detailed information about the :py:meth:`bf2.gameLogic.sendHudEvent <bf2.GameLogic.GameLogic.sendHudEvent>`. These events are categorized by number.

Event by Number
---------------

#. Close To Control Point
#. Hud State Changed
#. Hud Disable
#. Hud Enable
#. Init Loading Screen
#. Update Loading Screen
#. Set Loading Screen Debug
#. Remove Loading Screen
#. Map Zoom Changed
#. Map Static Changed
#. Squad Is Full
#. Squad Is Private
#. Squad Creation Failed
#. Squad Creation Success
#. Squad Invalid Name
#. Squad Invitation
#. Squad Join Request
#. Squad Join Request Denied

   :Data: 0 - 7
   :Data name: Squad ID
   :Results: This event displays a message: "Your request to join #SQUADNAME# squad has been denied." The squad name dynamically updates based on the provided Squad ID.

#. Squad Join Request Accepted

   :Data: 0 - 7
   :Data Name: Squad ID
   :Results: This event displays a message: "Your request to join #SQUADNAME# squad has been accepted." The squad name dynamically updates based on the provided Squad ID.

#. Kicked From Squad

   :Data: 0 - 255
   :Data Name: Player ID
   :Results: This event displays a message indicating a player was kicked from a squad, either "... has been kicked from your squad." or "You have been kicked from your squad," depending on the Player ID.

#. Left Squad

   :Data: 0 - 255
   :Data Name: Player ID
   :Results: This event displays a message: "... has left your squad." This message is only shown if the recipient is in a squad. If the Player ID matches the recipient, no action occurs.

#. Joined Squad

   :Data: 0 - 255
   :Data Name: Player ID
   :Results: This event displays a message: "... has joined your squad." This message is only shown if the recipient is in a squad. If the Player ID matches the recipient, no action occurs.

#. Squad Orders Received

   :Data: 0 - 255
   :Data Name: Player ID
   :Results: This event displays a message: "You have received a new order from your squadleader." The Player ID appears to have no effect on the message. No action occurs if the message is sent to the squad leader.

#. New Squad Leader

   :Data: 0 - 255
   :Data Name: Player ID
   :Results: This event displays a message indicating a new squad leader, either "... is your new squad leader" or "You are the new squad leader," depending on the Player ID.

#. Squad Leader Request
#. Commander Orders Received
#. Commander Orders Sent
#. Squad Orders Sent
#. Request Recieved
#. Request Sent
#. Update Hud
#. Weapon Changed
#. Commander Accept
#. Commander Decline
#. Commander Invitation
#. Squad LeaderInvitation
#. Commander Resign
#. Rank Change
#. Medal Reward
#. UAV
#. Satellite
#. Artillery
#. Unit Spotted
#. Missile Lock
#. New Unlock
#. Call For Medic
#. Call For Ammo
#. Call For Repair
#. Call For Revive
#. Auto Call For Revive
#. Radio Call
#. Was Hit
#. Possibly Not Used
#. Possibly Not Used
#. Possibly Not Used
#. Possibly Not Used
#. Is Close To Mine

   :Data: 0 - 255
   :Data Name: Player ID

#. Not Close To Mine

   :Data: 0 - 255
   :Data Name: Player ID

#. Muted By Remote
#. Possibly Not Used
#. TK Option
#. TK Response
#. Possibly Not Used
#. Control Point Taken
#. Control Point Lost
#. Enable Help Message

   :Data: 49
   :Data Name: Exit To Capture Flag

#. Enable Help
#. Possibly Not Used
#. Possibly Not Used
#. Ticket Bleed
#. Ticket State Changed
#. Begin Round
#. Possibly Not Used
#. Possibly Not Used
#. Map Change Complete
#. Map Zoom Complete

.. note::

   Some HUD events may trigger informative messages for in-game players. However, the HUD event itself does not cause these occurrences; instead, it merely sends the message that would typically be displayed if that event had actually taken place.
