#/bin/bash

sudo xboxdrv -s -d --deadzone 15% --trigger-as-button --dpad-as-button &
sudo python3 src/robot.py
sudo killall -r xboxdrv
