Last update: 2013-03-19

This directory holds three test scripts:
- a receiving script "mayapy_receive" which acts as our plugin's receiving end.
- a script which sends a message "mayapy_send" acts as MVN which sends us an udp message.
- a more sophisticated receiving script "mayapy_EULER" which can be used with 
  the real MVN Studio software to receive and examine 1 full message of 668 bytes.

Setup:
- Download python 3.x.
- On Windows machines open the python interpreter IDLE.
- On Unix and GNU/Linux machines open a shell. 
- Open and/or execute "mayapy_receive".
- Open and/or execute "mayapy_send", it will send a message to mayapy_receive.
  You can execute mayapy_send as many times as you want to receive new messages.

Note: i've only got MVN Studio and Maya 2012 to work on a Windows machine.


# Revision:
2013-03-19: Rewrote this file in English.
2012-04-19: Added Euler message that we've been using for research and testing.
