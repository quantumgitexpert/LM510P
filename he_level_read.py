import numpy as np
import serial
from time import sleep

def he_read():
    # return np.round(100 * np.random.rand(),decimals=2)
    dev = serial.Serial('COM10',timeout=5)

    # Send commands
    dev.write(b'MEAS 1\r\n')
    dev.write(b'REMOTE')
    dev.write(b'MODE S\r\n')
    dev.write(b'INTVL 10\r\n')

    dev.flush()
    dev.write(str.encode('MEAS 1\r\n'))
    dev.read_all()
    sleep(2)
    dev.flush()
    dev.write(b'MEAS? 1\r\n')
    res = dev.read_all()
    # print("MEAS? 1 response:", res.decode())
    
    sleep(1)
    res = dev.readline()
    # print("line1:", res.decode())
    res = dev.readline()
    # print("line2:", res.decode())
    res = dev.readline()
    # print("line3:", res.decode())
    res = dev.readline()
    # print("line4:", res.decode())
    

    # dev.write(str.encode('*IDN?\r\n'))
    # res = dev.read_all()
    # print("*IDN? response:", res.decode())

    # Close the serial connection
    dev.close()
    del dev

    return float(res[0:4])