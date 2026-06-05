from djitellopy import tello
from time import sleep

me=tello.Tello()
me.connect()
print(me.get_battery())
me.takeoff()
me.send_rc_control(0,30,0,0)#这里分别是左右前后的速度
sleep(2)
me.send_rc_control(60,0,0,0)#这里分别是左右前后的速度  1右2前4旋转
sleep(2)
me.send_rc_control(360,50,0,0)
sleep(2)
me.send_rc_control(400,0,0,0)
me.land()

