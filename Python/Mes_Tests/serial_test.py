#!/usr/bin/env python
# -*- coding: utf-8 -*-
# lsusb to check device name
# dmesg | grep "tty" to find port name

# ls -l /dev/ttyACM*
# sudo chmod a+rw /dev/ttyACM0
# restart IDE

import serial
import time

if __name__ == '__main__':

    print('Running. Press CTRL-C to exit.')
    with serial.Serial("/dev/ttyACM0", 9600, timeout=1) as arduino:
        time.sleep(0.1)  # wait for serial to open
        if arduino.isOpen():
            print("{} connected!".format(arduino.port))
            try:
                while True:
                    cmd = input("Enter command : ")
                    cmd2 = input("Enter command : ")
                    cmd = cmd + ',' + cmd2 + ','
                    arduino.write(cmd.encode())
                    # time.sleep(0.1) #wait for arduino to answer
                    while arduino.inWaiting() == 0: pass
                    if arduino.inWaiting() > 0:
                        answer = arduino.readline()
                        print(answer)
                        arduino.flushInput()  # remove data after reading
            except KeyboardInterrupt:
                print("KeyboardInterrupt has been caught.")