#/bin/bash

sudo xboxdrv -s -d --deadzone 15% &
sudo python3 src/robot.py
sudo killall -r xboxdrv
