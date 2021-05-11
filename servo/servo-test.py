from servo import Servo
import utime

pwmPin=15 #change for your pin
motor=Servo(pwmPin)

while True:
    motor.move(0)
    utime.sleep(1)
    motor.move(45)
    utime.sleep(1) 
    motor.move(90)
    utime.sleep(1)
    motor.move(135)
    utime.sleep(1)
    motor.move(180)
    utime.sleep(1)
