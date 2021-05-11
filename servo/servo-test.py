from servo import Servo
import utime

servo_pwm_freq = 50
min_u16_duty = 1000 - 400 # offset for correction
max_u16_duty = 6000  # offset for correction
min_angle = 0
max_angle = 180    
current_angle = 0.001


    
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