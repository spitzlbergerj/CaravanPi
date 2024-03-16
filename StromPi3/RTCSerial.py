import serial
import threading
from time import sleep
import time
import datetime
import os

serial_port = serial.Serial()

serial_port.baudrate = 38400
serial_port.port = '/dev/serial0'
serial_port.timeout = 1
serial_port.bytesize = 8
serial_port.stopbits = 1
serial_port.parity = serial.PARITY_NONE


if serial_port.isOpen(): serial_port.close()
serial_port.open()


try:
    serial_port.write(str.encode('Q'))
    sleep(1)
    serial_port.write(str.encode('\x0D'))
    sleep(1)
    serial_port.write(str.encode('date-rpi'))
    sleep(0.1)
    serial_port.write(str.encode('\x0D'))
    data = serial_port.read(9999);
    date = int(data)

    strompi_year = date // 10000
    strompi_month = date % 10000 // 100
    strompi_day = date % 100

    sleep(0.1)
    serial_port.write(str.encode('time-rpi'))
    sleep(0.1)
    serial_port.write(str.encode('\x0D'))
    data = serial_port.read(9999);
    timevalue = int(data)

    strompi_hour = timevalue // 10000
    strompi_min = timevalue % 10000 // 100
    strompi_sec = timevalue % 100

    rpi_time = datetime.datetime.now().replace(microsecond=0)
    strompi_time = datetime.datetime(2000 + strompi_year, strompi_month, strompi_day, strompi_hour, strompi_min, strompi_sec, 0)

    command = 'set-time %02d %02d %02d' % (int(rpi_time.strftime('%H')),int(rpi_time.strftime('%M')),int(rpi_time.strftime('%S')))

    if rpi_time > strompi_time:
        serial_port.write(str.encode('set-date %02d %02d %02d %02d' % (int(rpi_time.strftime('%d')),int(rpi_time.strftime('%m')),int(rpi_time.strftime('%Y'))%100,int(rpi_time.isoweekday()))))
        sleep(0.5)
        serial_port.write(str.encode('\x0D'))
        sleep(1)
        serial_port.write(str.encode('set-clock %02d %02d %02d' % (int(rpi_time.strftime('%H')),int(rpi_time.strftime('%M')),int(rpi_time.strftime('%S')))))
        sleep(0.5)
        serial_port.write(str.encode('\x0D'))

        print ('-----------------------------------------')
        print ('The date und time has been synced: Raspberry Pi -> StromPi')
        print ('-----------------------------------------')

    else:
        os.system('sudo date +%%y%%m%%d --set=%02d%02d%02d' % (strompi_year, strompi_month, strompi_day))
        os.system('sudo date +%%T -s "%02d:%02d:%02d"' % (strompi_hour, strompi_min, strompi_sec))
        print ('-----------------------------------------')
        print ('The date und time has been synced: StromPi -> Raspberry Pi')
        print ('-----------------------------------------')

except KeyboardInterrupt:
    print('interrupted!')

serial_port.close()