import serial
from time import sleep

dev = serial.Serial('COM10')

# Send commands
dev.write(b'MEAS 1\r\n')
dev.write(b'REMOTE')
dev.write(b'MODE S\r\n')
dev.write(b'INTVL 10\r\n')

dev.write(str.encode('MEAS 1\r\n'))

sleep(3)

dev.write(b'MEAS? 1\r\n')
res = dev.read_all()
print("MEAS? 1 response:", res.decode())

dev.write(str.encode('*IDN?\r\n'))
res = dev.read_all()
print("*IDN? response:", res.decode())

# Close the serial connection
dev.close()
del dev
