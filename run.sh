#/bin/bash

sudo xboxdrv -s -d &
sudo python3 src/robot.py
sudo killall -r xboxdrv
