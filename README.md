# PythonRobot

### Python Robot Project for Raspberry Pi 3B using the Monk Makes RasPiRobot Board V3 

https://www.monkmakes.com/rrb3/

https://www.monkmakes.com/pi-rover/

- Robot is controlled by an Xbox 360 wireless controller with a USB adaptor
- Raspberry Pi 3B powered by a 5V 2A 5000mAh micro USB battery
- Motors powered by a 6x AA battery pack 

## Software Prerequisites:

`sudo apt-get update`

`sudo apt-get install python3-dev python3-rpi.gpio python3-smbus python3-pip xboxdrv`

`sudo pip3 install evdev`


## Run Instructions:

1. Plug in and turn on Xbox 360 controller
2. Run the 'run.sh' script
3. Press 'Ctrl-C' or the 'Start' button to exit 

## Commands:

Commands are defined in src/robot.py

- Left Stick - Controls velocity of left wheel
- Right Stick - Controls velocity of right wheel
- A - Drive forward 24 inches; Uses Hall Effect encoders
- B - Drive forward at 12 inches/second; Uses Hall Effect encoders
- X - Drive until 12 inches away from object or wall; Uses Ultrasonic distance sensor
- Y - Turn to an angle of 45 degrees; Uses MPU6050 Gyroscope
- Start - Exits program
- Select - Follow path defined in src/commands/PursuitCommand.py; Uses Pure Pursuit

## Sensors:

- MPU6050 Gyroscope + Accelerometer
- HCSR04 Ultrasonic Sensor
- RB-DFR-668 Motor with Hall Effect Encoder

## Thanks to the Following GitHub Repositories:

https://github.com/simonmonk/raspirobotboard3

https://github.com/Tijndagamer/mpu6050
