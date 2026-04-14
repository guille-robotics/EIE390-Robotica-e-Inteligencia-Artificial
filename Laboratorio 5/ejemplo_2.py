from servo import Servo
from time import sleep

# Create a Servo object on pin 0
servo=Servo(pin=0)


try:
    while True:
        for i in range (0,180 + 1,10):
            servo.move(i)
            sleep(1)
            print(servo.get_current_angle())
            
except KeyboardInterrupt:
    print("Keyboard interrupt")
    # Turn off PWM 
    servo.stop()
