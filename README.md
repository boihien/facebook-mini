# Facebook-Mini
Project that emulates instant messaging feature from facebook messenger. Uses socket programming with a server/client template. The client interacts with the server and the server verifies the user's actions.

## Instructions:
* Install mininet on Virtual Box
* Copy files into mininet
* Enter command `sudo mn --custom finalTopol.py --topo myTopo -x`
* Enter command `python server2.py` in the S1 terminal window
* Enter command `python client2.py` in the C1 terminal window

## Features
The user can 
* Change password
* Logout
* Send message to another client (online/offline)
* View messages
* Broadcast messages
* Form groups (To be implemented)

## User Login Info
The usernames are hardcoded into the server. The current username and passwords are
* Username: User1 | Password: 123
* Username: User2 | Password: 123
* Username: User3 | Password: 123

## Quick Demo
![GitHub Logo](/ScreenShots/facebook-min-capture1)
* Logging into server

![GitHub Logo](/ScreenShots/facebook-min-capture2)
* Sending message to user2

![GitHub Logo](/ScreenShots/facebook-min-capture3)
* user2 recieving message
