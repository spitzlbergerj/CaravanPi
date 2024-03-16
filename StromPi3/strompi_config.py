import serial
from time import sleep
import datetime
import os
import time
from time import sleep

wide_range_volt_min = 4.8
battery_volt_min = 0.5
mUSB_volt_min = 4.1

breakS = 0.1
breakL = 0.5

serial_port = serial.Serial()

serial_port.baudrate = 38400
serial_port.port = '/dev/serial0'
serial_port.timeout = 1
serial_port.bytesize = 8
serial_port.stopbits = 1
serial_port.parity = serial.PARITY_NONE

if serial_port.isOpen(): serial_port.close()
serial_port.open()

#######################################################################################################################

def enabled_disabled_converter(argument):
    switcher = {
        0: 'Disabled',
        1: 'Enabled',
    }
    return switcher.get(argument, 'nothing')

def weekday_converter(argument):
    switcher = {
        1: 'Monday',
        2: 'Tuesday',
        3: 'Wednesday',
        4: 'Thursday',
        5: 'Friday',
        6: 'Saturday',
        7: 'Sunday',
    }
    return switcher.get(argument, 'nothing')

def strompi_mode_converter(argument):
    switcher = {
        1: 'mUSB -> Wide',
        2: 'Wide -> mUSB',
        3: 'mUSB -> Battery',
        4: 'Wide -> Battery',
        5: "mUSB -> Wide -> Battery",
        6: "Wide -> mUSB -> Battery",
    }
    return switcher.get(argument, 'nothing')

def alarm_mode_converter(argument):
    switcher = {
        1: 'Time-Alarm',
        2: 'Date-Alarm',
        3: 'Weekday-Alarm',
        4: 'Wakeup Timer',
    }
    return switcher.get(argument, 'nothing')

def batterylevel_shutdown_converter(argument):
    switcher = {
        0: 'Disabled',
        1: '10%',
        2: '25%',
        3: '50%',
    }
    return switcher.get(argument, 'nothing')

def output_status_converter(argument):
    switcher = {
        0: 'Power-Off', #only for Debugging-Purposes
        1: 'mUSB',
        2: 'Wide',
        3: 'Battery',
    }
    return switcher.get(argument, 'nothing')


def batterylevel_converter(batterylevel,charging):

    if charging:
        switcher = {
            1: ' [10%] [charging]',
            2: ' [25%] [charging]',
            3: ' [50%] [charging]',
            4: ' [100%] [charging]',
        }
        return switcher.get(batterylevel, 'nothing')
    else:
        switcher = {
            1: ' [10%]',
            2: ' [25%]',
            3: ' [50%]',
            4: ' [100%]',
        }
        return switcher.get(batterylevel, 'nothing')

#######################################################################################################################
serial_port.write(str.encode('quit'))
sleep(breakS)
serial_port.write(str.encode('\x0D'))
sleep(breakL)

serial_port.write(str.encode('status-rpi'))
sleep(1)
serial_port.write(str.encode('\x0D'))
sp3_time = serial_port.readline(9999);
sp3_date = serial_port.readline(9999);
sp3_weekday = serial_port.readline(9999);
sp3_modus = serial_port.readline(9999);
sp3_alarm_enable = serial_port.readline(9999);
sp3_alarm_mode = serial_port.readline(9999);
sp3_alarm_hour = serial_port.readline(9999);
sp3_alarm_min = serial_port.readline(9999);
sp3_alarm_day = serial_port.readline(9999);
sp3_alarm_month = serial_port.readline(9999);
sp3_alarm_weekday = serial_port.readline(9999);
sp3_alarmPoweroff = serial_port.readline(9999);
sp3_alarm_hour_off = serial_port.readline(9999);
sp3_alarm_min_off = serial_port.readline(9999);
sp3_shutdown_enable = serial_port.readline(9999);
sp3_shutdown_time = serial_port.readline(9999);
sp3_warning_enable = serial_port.readline(9999);
sp3_serialLessMode = serial_port.readline(9999);
sp3_intervalAlarm = serial_port.readline(9999);
sp3_intervalAlarmOnTime = serial_port.readline(9999);
sp3_intervalAlarmOffTime = serial_port.readline(9999);
sp3_batLevel_shutdown = serial_port.readline(9999);
sp3_batLevel = serial_port.readline(9999);
sp3_charging = serial_port.readline(9999);
sp3_powerOnButton_enable = serial_port.readline(9999);
sp3_powerOnButton_time = serial_port.readline(9999);
sp3_powersave_enable = serial_port.readline(9999);
sp3_poweroffMode = serial_port.readline(9999);
sp3_poweroff_time_enable = serial_port.readline(9999);
sp3_poweroff_time = serial_port.readline(9999);
sp3_wakeupweekend_enable = serial_port.readline(9999);
sp3_ADC_Wide = float(serial_port.readline(9999))/1000;
sp3_ADC_BAT = float(serial_port.readline(9999))/1000;
sp3_ADC_USB = float(serial_port.readline(9999))/1000;
sp3_ADC_OUTPUT = float(serial_port.readline(9999))/1000;
sp3_output_status = serial_port.readline(9999);
sp3_powerfailure_counter = serial_port.readline(9999);
sp3_firmwareVersion = serial_port.readline(9999);
powerofftime_enabletest = (str(sp3_poweroff_time_enable, 'utf-8').rstrip('\n').zfill(2))
date = int(sp3_date)

strompi_year = int(sp3_date) // 10000
strompi_month = int(sp3_date) % 10000 // 100
strompi_day = int(sp3_date) % 100

strompi_hour = int(sp3_time) // 10000
strompi_min = int(sp3_time) % 10000 // 100
strompi_sec = int(sp3_time) % 100

try:
    print('###########################################################################')
    print('\rStromPi V3 Serial Config Script (PYTHON3)\r')
    print('###########################################################################')

    print('\n---------------------------------------------------------------------------')
    print('  Main Configuration')
    print('---------------------------------------------------------------------------')

    #strompi-mode
    print('[StromPi-Mode: ' + sp3_modus.decode(encoding='UTF-8', errors='strict').rstrip('\n') + ' (' + strompi_mode_converter((int(sp3_modus))) + ')]')
    print('\nSetting the StromPi mode \n(1 = mUSB -> Wide, 2 = Wide -> mUSB, 3 = mUSB -> Battery, 4 = Wide -> Battery, 5 = mUSB -> Wide -> Battery, 6 = Wide -> mUSB -> Battery)\n')
    sp3_modus_temp = int(sp3_modus)
    sp3_modus = input('Mode (1-6): ')
    while int(sp3_modus) < 1 or int(sp3_modus) > 6:
        sp3_modus = input('Failed! Value not in Range - Please try again\nMode (1-6): ')

    if sp3_modus_temp != int(sp3_modus):
        modusreset = 1
    else:
        modusreset = 0

    print('\n--------------------------------------')
    #Shutdown-enable & set-timer
    print('[Raspberry Pi Shutdown: ' + enabled_disabled_converter(int(sp3_shutdown_enable)) + ']')
    print('\nEnabling or disabling the Raspberry Pi shutdown (0 = disable, 1 = enable)\n')

    sp3_shutdown_enable	 = input('Shutdown enable/disable (0 - 1): ')
    while int(sp3_shutdown_enable	) < 0 or int(sp3_shutdown_enable	) > 1:
        sp3_shutdown_enable	 = input('Failed! Value not in Range - Please try again\nShutdown status (0 - 1): ')

    if int(sp3_shutdown_enable	) == 1:
        print('\n--------------------------------------')
        print('[Shutdown-Timer: ' + str(sp3_shutdown_time, 'utf-8').rstrip('\n').zfill(2) + ' seconds' + ']')
        print('\nSetting shutdown timer (seconds)\n')

        sp3_shutdown_time = input('Seconds (0 - 65535): ')
        while int(sp3_shutdown_time) < 0 or int(sp3_shutdown_time) > 65535:
            sp3_shutdown_time = input('Failed! Value not in Range - Please try again\nSeconds (0 - 65535): ')

    #batlevel-shutdown
    print('\n--------------------------------------')
    print('[Battery-Level Shutdown: ' + batterylevel_shutdown_converter(int(sp3_batLevel_shutdown)) + ']')
    print('\nSetting battery level shutdown (0 = disable, 1 = below 10%, 2 = below 25%, 3 = below 50%)\n')

    sp3_batLevel_shutdown = input('Battery level shutdown (0 - 3): ')
    while int(sp3_batLevel_shutdown) < 0 or int(sp3_batLevel_shutdown) > 3:
        sp3_batLevel_shutdown = input('Failed! Value not in Range - Please try again\nBattery level shutdown (0 - 3): ')


    #serialless-mode
    print('\n--------------------------------------')
    print('[Serial-Less Mode: ' + enabled_disabled_converter(int(sp3_serialLessMode)) + ']')
    print('\nEnabling or disabling serialless-mode (0 = disable, 1 = enable)\n')

    sp3_serialLessMode = input('Serialless mode (0 - 1): ')
    while int(sp3_serialLessMode) < 0 or int(sp3_serialLessMode) > 1:
        sp3_serialLessMode = input('Failed! Value not in Range - Please try again\nSerialless mode (0 - 1): ')

    #powersave
    print('\n--------------------------------------')
    print('[Power Save Mode: ' + enabled_disabled_converter(int(sp3_powersave_enable)) + ']')
    print('\nEnabling or disabling the Power Save mode (0 = disable, 1 = enable)\n')

    sp3_powersave_enable = input('Power Save mode (0 - 1): ')
    while int(sp3_powersave_enable) < 0 or int(sp3_powersave_enable) > 1:
        sp3_powersave_enable = input('Failed! Value not in Range - Please try again\nPower Save mode (0 - 1): ')


    #warning-enable
    print('\n--------------------------------------')
    print('[Powerfail Warning: ' + enabled_disabled_converter(int(sp3_warning_enable)) + ']')
    print('\nEnabling or disabling the Powerfail-Warning (instead of a shutdown) through the serial interface  (0 = disable, 1 = enable)\n')

    sp3_warning_enable = input('Warning enable/disable (0 - 1): ')
    while int(sp3_warning_enable) < 0 or int(sp3_warning_enable) > 1:
        sp3_warning_enable = input('Failed! Value not in Range - Please try again\nWarning status (0 - 1): ')

    print('\n--------------------------------------')
    # PowerOn-Button Enable & PowerOn-Button Timer
    print('[PowerOn-Button: ' + enabled_disabled_converter(int(sp3_powerOnButton_enable)) + ']')
    print('\nEnabling or disabling the PowerOn-Button Feature (0 = disable, 1 = enable)\n')

    sp3_powerOnButton_enable = input('PowerOn-Button enable/disable (0 - 1): ')
    while int(sp3_powerOnButton_enable) < 0 or int(sp3_powerOnButton_enable) > 1:
        sp3_powerOnButton_enable = input('Failed! Value not in Range - Please try again\nShutdown status (0 - 1): ')
		
    if int(sp3_powerOnButton_enable) == 1 and int(sp3_shutdown_enable) == 1:
        print('\n--------------------------------------')
        print('[Poweroff Mode: ' + enabled_disabled_converter(int(sp3_poweroffMode)) + ']')
		
        sp3_poweroffMode = input('Poweroff Mode enable/disable (0 - 1): ')
        while int(sp3_poweroffMode) < 0 or int(sp3_poweroffMode) > 1:
            sp3_poweroffMode = input('Failed! Value not in Range - Please try again\nPoweroff Mode status (0 - 1): ')

    if int(sp3_powerOnButton_enable) == 1:
        print('\n--------------------------------------')
        print('[PowerOn-Button Initialization Time: ' + str(sp3_powerOnButton_time, 'utf-8').rstrip('\n').zfill(2) + ' seconds' + ']')
        print('\nPowerOn-Button Initialization Time: (seconds)\n')

        sp3_powerOnButton_time = input('Seconds (0 - 65535): ')
        while int(sp3_powerOnButton_time) < 0 or int(sp3_powerOnButton_time) > 65535:
            sp3_powerOnButton_time = input('Failed! Value not in Range - Please try again\nSeconds (0 - 65535): ')

    print('\n---------------------------------------------------------------------------')
    print(' Time&Date-Configuration')
    print('---------------------------------------------------------------------------')
    #set-clock
    print('[Actual Raspberry Pi Time&Date]')
    print('[Time: ' + str(strompi_hour).zfill(2) + ':' + str(strompi_min).zfill(2) + ':' + str(strompi_sec).zfill(2) + ']')
    print('[Date: ' + weekday_converter(int(sp3_weekday)) + ' ' + str(strompi_day).zfill(2) + '.' + str(strompi_month).zfill(
        2) + '.' + str(strompi_year).zfill(2) + ']')

    timeconfig = input('\nDo you want to change the Time&Date-Configuration? (Y) Yes | (N) No:')
    while not (timeconfig == 'Y' or timeconfig == 'N'):
        timeconfig = input('Failed! Value not in Range - Please try again\nDo you want to change the Alarm-Configuration? (Y) Yes | (N) No: ')

    if timeconfig == 'Y':

        internettime = input(
            'Do you want to change the Time&Date Manual\n or do you want to transfer the actual SystemTime of the Raspberry Pi (S) Systemtime | (M) Manual:')
        while not (internettime == 'S' or internettime == 'M'):
            internettime = input(
                'Failed! Value not in Range - Please try again\nDo you want to change the Alarm-Configuration? (Y) Yes | (N) No: ')

        if internettime == 'S':

            print('-----------------------------------------')
            print('TimeSync-Process | Please Wait')
            print('-----------------------------------------')

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
            strompi_time = datetime.datetime(2000 + strompi_year, strompi_month, strompi_day, strompi_hour, strompi_min,
                                             strompi_sec, 0)

            if rpi_time > strompi_time:
                serial_port.write(str.encode('set-date %02d %02d %02d %02d' % (
                    int(rpi_time.strftime('%d')), int(rpi_time.strftime('%m')), int(rpi_time.strftime('%Y')) % 100,
                    int(rpi_time.isoweekday()))))
                sleep(0.5)
                serial_port.write(str.encode('\x0D'))
                sleep(1)
                serial_port.write(str.encode('set-clock %02d %02d %02d' % (
                    int(rpi_time.strftime('%H')), int(rpi_time.strftime('%M')), int(rpi_time.strftime('%S')))))
                sleep(0.5)
                serial_port.write(str.encode('\x0D'))

                print ('-----------------------------------------')
                print ('The date und time has been synced: Raspberry Pi -> StromPi')
                print ('-----------------------------------------')


        elif internettime == 'M':
            print('\n--------------------------------------')
            print('\nSetting the clock (hour, minute)\n')

            setClockH = input('Hour (0-23): ')
            while int(setClockH) < 0 or int(setClockH) > 23:
                setClockH = input('Failed! Value not in Range - Please try again\nHour (0-23): ')

            setClockM = input('Minute (0-59): ')
            while int(setClockM) < 0 or int(setClockM) > 59:
                setClockM = input('Failed! Value not in Range - Please try again\nMinute (0-59): ')

            setClockS = '00'

            # set-date
            print('\n--------------------------------------')
            print('\nSetting the date (day, month, year, weekday)\n')

            setDateD = input('Day (1-31): ')
            while int(setDateD) < 1 or int(setDateD) > 31:
                setDateD = input('Failed! Value not in Range - Please try again\nDay (1-31): ')

            setDateM = input('Month (1-12): ')
            while int(setDateM) < 1 or int(setDateM) > 12:
                setDateM = input('Failed! Value not in Range - Please try again\nMonth (1-12): ')

            setDateY = input('Year (0-99): ')
            while int(setDateY) < 0 or int(setDateY) > 99:
                setDateY = input('Failed! Value not in Range - Please try again\nYear (0-99): ')

            setDateWD = input(
                'Weekday (1 = Monday, 2 = Tuesday, 3 = Wednesday, 4 = Thursday, 5 = Friday, 6 = Saturday, 7 = Sunday): ')
            while int(setDateWD) < 1 or int(setDateWD) > 7:
                setDateWD = input(
                    'Failed! Value not in Range - Please try again\nWeekday (1 = Monday, 2 = Tuesday, 3 = Wednesday, 4 = Thursday, 5 = Friday, 6 = Saturday, 7 = Sunday): ')

            serial_port.write(str.encode('quit'))
            sleep(breakS)
            serial_port.write(str.encode('\x0D'))
            sleep(breakL)

            serial_port.write(str.encode('set-date ' + setDateD + ' ' + setDateM + ' ' + setDateY + ' ' + setDateWD))
            sleep(breakS)
            serial_port.write(str.encode('\x0D'))
            print('\n\nSetting set-date...')
            sleep(breakL)

            serial_port.write(str.encode('set-clock ' + setClockH + ' ' + setClockM + ' ' + setClockS))
            sleep(breakS)
            serial_port.write(str.encode('\x0D'))
            print('Setting set-clock...')
            sleep(breakL)

    print('\n---------------------------------------------------------------------------')
    print(' Alarm-Configuration')
    print('---------------------------------------------------------------------------')

    print('[Actual Raspberry Pi Time&Date]')
    if powerofftime_enabletest == "01":
        print(' Alarm-Mode: Wakeup Timer')
    else:
        print(' Alarm-Mode: ' + alarm_mode_converter(int(sp3_alarm_mode)))
    print(
        ' Alarm-Time: ' + str(sp3_alarm_hour, 'utf-8').rstrip('\n').zfill(2) + ':' + str(sp3_alarm_min, 'utf-8').rstrip(
            '\n').zfill(2))
    print(' Alarm-Date: ' + str(sp3_alarm_day, 'utf-8').rstrip('\n').zfill(2) + '.' + str(sp3_alarm_month,
                                                                                          'utf-8').rstrip(
        '\n').zfill(2))
    print(' WakeUp-Alarm: ' + weekday_converter(int(sp3_alarm_weekday)))
    print(' ')
    print('PowerOff-Alarm: ' + enabled_disabled_converter(int(sp3_alarmPoweroff)))
    print(
        ' PowerOff-Alarm-Time: ' + str(sp3_alarm_hour_off, 'utf-8').rstrip('\n').zfill(2) + ':' + str(sp3_alarm_min_off,
                                                                                                      'utf-8').rstrip(
            '\n').zfill(2))
    print(' ')
    print('Interval-Alarm: ' + enabled_disabled_converter(int(sp3_intervalAlarm)))
    print(' Interval-On-Time: ' + str(sp3_intervalAlarmOnTime, 'utf-8').rstrip('\n').zfill(2) + ' minutes')
    print(' Interval-Off-Time: ' + str(sp3_intervalAlarmOffTime, 'utf-8').rstrip('\n').zfill(2) + ' minutes')
    print(' ')

    alarmconfig = '0'
    alarmconfig = input('Do you want to change the Alarm-Configuration? (Y) Yes | (N) No:')
    while not (alarmconfig == 'Y' or alarmconfig == 'N'):
        alarmconfig = input(
            'Failed! Value not in Range - Please try again\nDo you want to change the Alarm-Configuration? (Y) Yes | (N) No: ')

    if alarmconfig == 'Y':

        print('\n----------------------------------------------')
        print(' Power-Off Alarm Configuration')
        print('-----------------------------------------------')

        alarmconfig = '0'
        alarmconfig = input('Do you want to change the Power-Off Alarm-Configuration? (Y) Yes | (N) No:')
        while not (alarmconfig == 'Y' or alarmconfig == 'N'):
            alarmconfig = input(
                'Failed! Value not in Range - Please try again\nDo you want to change the Alarm-Configuration? (Y) Yes | (N) No: ')

        if alarmconfig == 'Y':
            # poweroff-enable & poweroff-set-time
            print('\n--------------------------------------')
            print('Enabling or disabling poweroff (0 = disable, 1 = enable)\n')

            sp3_alarmPoweroff = input('Poweroff status (0 - 1): ')
            while int(sp3_alarmPoweroff) < 0 or int(sp3_alarmPoweroff) > 1:
                sp3_alarmPoweroff = input('Failed! Value not in Range - Please try again\nPoweroff status (0 - 1): ')

            if int(sp3_alarmPoweroff) == 1:
                print('\n--------------------------------------')
                print('Setting poweroff time (hour, minute)\n')

                sp3_alarm_hour_off = input('Hour (0 - 23): ')
                while int(sp3_alarm_hour_off) < 0 or int(sp3_alarm_hour_off) > 23:
                    sp3_alarm_hour_off = input('Failed! Value not in Range - Please try again\nHour (0 - 23): ')

                sp3_alarm_min_off = input('Minute (0 - 59): ')
                while int(sp3_alarm_min_off) < 0 or int(sp3_alarm_min_off) > 59:
                    sp3_alarm_min_off = input('Failed! Value not in Range - Please try again\nMinute (0 - 59): ')

        print('\n---------------------------------------------------------------------------')
        print(' Wake-Up Alarm-Configuration')
        print('---------------------------------------------------------------------------')

        alarmconfig = '0'
        alarmconfig = input('Do you want to change the Wake-Up Alarm-Configuration? (Y) Yes | (N) No:')
        while not (alarmconfig == 'Y' or alarmconfig == 'N'):
            alarmconfig = input(
                'Failed! Value not in Range - Please try again\nDo you want to change the Alarm-Configuration? (Y) Yes | (N) No: ')

        if alarmconfig == 'Y':
            print('\n--------------------------------------')
            # alarm-enable & alarm-mode
            print('\nEnabling or disabling wake up alarm (0 = disable, 1 = enable)\n')

            sp3_alarm_enable = input('Wake up alarm status (0 - 1): ')
            while int(sp3_alarm_enable) < 0 or int(sp3_alarm_enable) > 1:
                sp3_alarm_enable = input(
                    'Failed! Value not in Range - Please try again\nWake up alarm status (0 - 1): ')

            if int(sp3_alarm_enable) == 1:
                print('\n--------------------------------------')
                print('Setting the wake up alarm mode (1 = Time-Alarm , 2 = Date-Alarm, 3 = Weekday-Alarm, 4 = Wakeup Timer)\n')

                sp3_alarm_mode = input('Wake up alarm mode (1 - 4): ')
                while int(sp3_alarm_mode) < 1 or int(sp3_alarm_mode) > 4:
                    sp3_alarm_mode = input('Failed! Value not in Range - Please try again\nWake up alarm mode (1 - 4): ')
                if int(sp3_alarm_mode) == 4:
                    print('\n--------------------------------------')
                    print('Set the wake up Timer\n')

                    sp3_poweroff_time = input('Wake up Timer (1-65535): ')
                    while int(sp3_poweroff_time) < 1 or int(sp3_poweroff_time) > 65535:
                        sp3_poweroff_time = input('Failed! Value not in Range - Please try again\nWake up Timer (1-65535): ')

                # Wake up alarm time
                if int(sp3_alarm_mode) == 1:
                    print('\n--------------------------------------')
                    print('Setting the wake up alarm time (hours, minutes)\n')

                    sp3_alarm_hour = input('Hours (0-23): ')
                    while int(sp3_alarm_hour) < 0 or int(sp3_alarm_hour) > 23:
                        sp3_alarm_hour = input('Failed! Value not in Range - Please try again\nHours (0-23): ')

                    sp3_alarm_min = input('Minutes (0-59): ')
                    while int(sp3_alarm_min) < 0 or int(sp3_alarm_min) > 59:
                        sp3_alarm_min = input('Failed! Value not in Range - Please try again\nHours (0-59): ')

                    sp3_wakeupweekend_enable = input('Wakeup Weekend mode (0-1): ')
                    while int(sp3_wakeupweekend_enable) < 0 or int(sp3_wakeupweekend_enable) > 1:
                        sp3_wakeupweekend_enable = input('Failed! Value not in Range - Please try again\nDisable Enable (0 - 1): ')
                # Wake up alarm date
                elif int(sp3_alarm_mode) == 2:
                    print('\n--------------------------------------')
                    print('Setting the wake up alarm date (day, month)\n')

                    sp3_alarm_day = input('Day (1-31): ')
                    while int(sp3_alarm_day) < 1 or int(sp3_alarm_day) > 31:
                        sp3_alarm_day = input('Failed! Value not in Range - Please try again\nDay (1-31): ')

                    sp3_alarm_month = input('Month (1-12): ')
                    while int(sp3_alarm_month) < 1 or int(sp3_alarm_month) > 12:
                        sp3_alarm_month = input('Failed! Value not in Range - Please try again\nMonth (1-12): ')

                else:
                    print('\n--------------------------------------')
                    print(
                        'Setting the wake up alarm date (1 = Monday, 2 = Tuesday, 3 = Wednesday, 4 = Thursday, 5 = Friday, 6 = Saturday, 7 = Sunday)\n')

                    sp3_alarm_weekday = input('Weekday (1 - 7): ')
                    while int(sp3_alarm_weekday) < 1 or int(sp3_alarm_weekday) > 7:
                        sp3_alarm_weekday = input('Failed! Value not in Range - Please try again\nWeekday (1 - 7): ')

        print('\n----------------------------------------------')
        print(' Interval-Alarm Configuration')
        print('-----------------------------------------------')

        alarmconfig = '0'
        alarmconfig = input('Do you want to change the Interval-Alarm-Configuration? (Y) Yes | (N) No:')
        while not (alarmconfig == 'Y' or alarmconfig == 'N'):
            alarmconfig = input(
                'Failed! Value not in Range - Please try again\nDo you want to change the Alarm-Configuration? (Y) Yes | (N) No: ')

        if alarmconfig == 'Y':
            # poweroff-enable & poweroff-set-time
            print('\n--------------------------------------')
            print('\nEnabling or disabling the Interval-Alarm (0 = disable, 1 = enable)\n')

            sp3_intervalAlarm = input('Interval-Alarm status (0 - 1): ')
            while int(sp3_intervalAlarm) < 0 or int(sp3_intervalAlarm) > 1:
                sp3_intervalAlarm = input(
                    'Failed! Value not in Range - Please try again\nInterval-Alarm status (0 - 1): ')

            if int(sp3_intervalAlarm) == 1:
                print('\n--------------------------------------')
                print('\nSetting Interval-Time Settings\n')

                sp3_intervalAlarmOnTime = input('Interval On-Time in minutes (1-65535): ')
                while int(sp3_intervalAlarmOnTime) < 1 or int(sp3_intervalAlarmOnTime) > 65535:
                    sp3_intervalAlarmOnTime = input(
                        'Failed! Value not in Range - Please try again\nInterval On-Time in minutes (1-65535): ')

                sp3_intervalAlarmOffTime = input('Interval Off-Time in minutes (1-65535): ')
                while int(sp3_intervalAlarmOffTime) < 0 or int(sp3_intervalAlarmOffTime) > 65535:
                    sp3_intervalAlarmOffTime = input(
                        'Failed! Value not in Range - Please try again\nInterval Off-Time in minutes (1-65535): ')


#######################################################################################################################

    print('\n----------------------------------------------')
    print(' Configuration Successful')
    print(' Transfer new Configuration to the StromPi 3')
    print(' \n###Please Wait###')
    print('-----------------------------------------------')

    breakS = 0.1
    breakL = 0.2


    if type(sp3_modus) == str:
        serial_port.write(str.encode('set-config ' + '1 ' +  sp3_modus))
    else:
        serial_port.write(str.encode('set-config ' + '1 ' + sp3_modus.decode(encoding='UTF-8', errors='strict')))
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)

    if sp3_alarm_mode == "1":
        serial_port.write(str.encode('set-config ' + '2 0'))
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)

        serial_port.write(str.encode('set-config ' + '3 0'))
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)

        serial_port.write(str.encode('set-config ' + '4 1'))
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)
		
        serial_port.write(str.encode('set-config ' + '26 0'))
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)

    elif sp3_alarm_mode == "2":
        serial_port.write(str.encode('set-config ' + '2 1'))
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)

        serial_port.write(str.encode('set-config ' + '3 0'))
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)

        serial_port.write(str.encode('set-config ' + '4 0'))
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)
		
        serial_port.write(str.encode('set-config ' + '26 0'))
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)

    elif sp3_alarm_mode == "3":
        serial_port.write(str.encode('set-config ' + '2 0'))
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)

        serial_port.write(str.encode('set-config ' + '3 1'))
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)

        serial_port.write(str.encode('set-config ' + '4 0'))
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)
		
        serial_port.write(str.encode('set-config ' + '26 0'))
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)
		
    elif sp3_alarm_mode == "4":
        serial_port.write(str.encode('set-config ' + '2 0'))
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)

        serial_port.write(str.encode('set-config ' + '3 0'))
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)

        serial_port.write(str.encode('set-config ' + '4 0'))
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)
		
        serial_port.write(str.encode('set-config ' + '26 1'))
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)
		

    if type(sp3_alarmPoweroff) == str:
        serial_port.write(str.encode('set-config ' + '5 ' +  sp3_alarmPoweroff))
    else:
        serial_port.write(str.encode('set-config ' + '5 ' + sp3_alarmPoweroff.decode(encoding='UTF-8', errors='strict')))
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)

    if type(sp3_alarm_min) == str:
        serial_port.write(str.encode('set-config ' + '6 ' +  sp3_alarm_min))
    else:
        serial_port.write(str.encode('set-config ' + '6 ' + sp3_alarm_min.decode(encoding='UTF-8', errors='strict')))
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)

    if type(sp3_alarm_hour) == str:
        serial_port.write(str.encode('set-config ' + '7 ' +  sp3_alarm_hour))
    else:
        serial_port.write(str.encode('set-config ' + '7 ' + sp3_alarm_hour.decode(encoding='UTF-8', errors='strict')))
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)

    if type(sp3_alarm_min_off) == str:
        serial_port.write(str.encode('set-config ' + '8 ' + sp3_alarm_min_off))
    else:
        serial_port.write(str.encode('set-config ' + '8 ' + sp3_alarm_min_off.decode(encoding='UTF-8', errors='strict')))
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)

    if type(sp3_alarm_hour_off) == str:
        serial_port.write(str.encode('set-config ' + '9 ' + sp3_alarm_hour_off))
    else:
        serial_port.write(str.encode('set-config ' + '9 ' + sp3_alarm_hour_off.decode(encoding='UTF-8', errors='strict')))
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)

    if type(sp3_alarm_day) == str:
        serial_port.write(str.encode('set-config ' + '10 ' + sp3_alarm_day))
    else:
        serial_port.write(str.encode('set-config ' + '10 ' + sp3_alarm_day.decode(encoding='UTF-8', errors='strict')))
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)

    if type(sp3_alarm_month) == str:
        serial_port.write(str.encode('set-config ' + '11 ' + sp3_alarm_month))
    else:
        serial_port.write(str.encode('set-config ' + '11 ' + sp3_alarm_month.decode(encoding='UTF-8', errors='strict')))
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)

    if type(sp3_alarm_weekday) == str:
        serial_port.write(str.encode('set-config ' + '12 ' + sp3_alarm_weekday))
    else:
        serial_port.write(str.encode('set-config ' + '12 ' + sp3_alarm_weekday.decode(encoding='UTF-8', errors='strict')))
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)

    if type(sp3_alarm_enable) == str:
        serial_port.write(str.encode('set-config ' + '13 ' + sp3_alarm_enable))
    else:
        serial_port.write(str.encode('set-config ' + '13 ' + sp3_alarm_enable.decode(encoding='UTF-8', errors='strict')))
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)

    if type(sp3_shutdown_enable) == str:
        serial_port.write(str.encode('set-config ' + '14 ' + sp3_shutdown_enable))
    else:
        serial_port.write(str.encode('set-config ' + '14 ' + sp3_shutdown_enable.decode(encoding='UTF-8', errors='strict')))
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)

    if type(sp3_shutdown_time) == str:
        serial_port.write(str.encode('set-config ' + '15 ' + sp3_shutdown_time))
    else:
        serial_port.write(str.encode('set-config ' + '15 ' + sp3_shutdown_time.decode(encoding='UTF-8', errors='strict')))
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)

    if type(sp3_warning_enable) == str:
        serial_port.write(str.encode('set-config ' + '16 ' + sp3_warning_enable))
    else:
        serial_port.write(str.encode('set-config ' + '16 ' + sp3_warning_enable.decode(encoding='UTF-8', errors='strict')))
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)

    if type(sp3_serialLessMode) == str:
        serial_port.write(str.encode('set-config ' + '17 ' + sp3_serialLessMode))
    else:
        serial_port.write(str.encode('set-config ' + '17 ' + sp3_serialLessMode.decode(encoding='UTF-8', errors='strict')))
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)

    if type(sp3_batLevel_shutdown) == str:
        serial_port.write(str.encode('set-config ' + '18 ' + sp3_batLevel_shutdown))
    else:
        serial_port.write(str.encode('set-config ' + '18 ' + sp3_batLevel_shutdown.decode(encoding='UTF-8', errors='strict')))
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)

    if type(sp3_intervalAlarm) == str:
        serial_port.write(str.encode('set-config ' + '19 ' + sp3_intervalAlarm))
    else:
        serial_port.write(str.encode('set-config ' + '19 ' + sp3_intervalAlarm.decode(encoding='UTF-8', errors='strict')))
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)

    if type(sp3_intervalAlarmOnTime) == str:
        serial_port.write(str.encode('set-config ' + '20 ' + sp3_intervalAlarmOnTime))
    else:
        serial_port.write(str.encode('set-config ' + '20 ' + sp3_intervalAlarmOnTime.decode(encoding='UTF-8', errors='strict')))
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)

    if type(sp3_intervalAlarmOffTime) == str:
        serial_port.write(str.encode('set-config ' + '21 ' + sp3_intervalAlarmOffTime))
    else:
        serial_port.write(str.encode('set-config ' + '21 ' + sp3_intervalAlarmOffTime.decode(encoding='UTF-8', errors='strict')))
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)

    if type(sp3_powerOnButton_enable) == str:
        serial_port.write(str.encode('set-config ' + '22 ' + sp3_powerOnButton_enable))
    else:
        serial_port.write(str.encode('set-config ' + '22 ' + sp3_powerOnButton_enable.decode(encoding='UTF-8', errors='strict')))
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)

    if type(sp3_powerOnButton_time) == str:
        serial_port.write(str.encode('set-config ' + '23 ' + sp3_powerOnButton_time))
    else:
        serial_port.write(str.encode('set-config ' + '23 ' + sp3_powerOnButton_time.decode(encoding='UTF-8', errors='strict')))
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)

    if type(sp3_powersave_enable) == str:
        serial_port.write(str.encode('set-config ' + '24 ' + sp3_powersave_enable))
    else:
        serial_port.write(str.encode('set-config ' + '24 ' + sp3_powersave_enable.decode(encoding='UTF-8', errors='strict')))
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)
	
    if type(sp3_poweroffMode) == str:
        serial_port.write(str.encode('set-config ' + '25 ' + sp3_poweroffMode))
    else:
        serial_port.write(str.encode('set-config ' + '25 ' + sp3_poweroffMode.decode(encoding='UTF-8', errors='strict')))
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)
    
    if type(sp3_poweroff_time) == str:
        serial_port.write(str.encode('set-config ' + '27 ' + sp3_poweroff_time))
    else:
        serial_port.write(str.encode('set-config ' + '27 ' + sp3_poweroff_time.decode(encoding='UTF-8', errors='strict')))
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)
	
    if type(sp3_wakeupweekend_enable) == str:
        serial_port.write(str.encode('set-config ' + '28 ' + sp3_wakeupweekend_enable))
    else:
        serial_port.write(str.encode('set-config ' + '28 ' + sp3_wakeupweekend_enable.decode(encoding='UTF-8', errors='strict')))
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)
	
    if modusreset == 1:
        serial_port.write(str.encode('set-config ' + '0 1'))
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)


    elif modusreset != 1:
        serial_port.write(str.encode('set-config ' + '0 0'))
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)

    print('\n----------------------------------------------')
    print(' Transfer Successful')
    print('-----------------------------------------------')

    serial_port.write(str.encode('status-rpi'))
    sleep(0.1)
    serial_port.write(str.encode('\x0D'))
    sp3_time = serial_port.readline(9999);
    sp3_date = serial_port.readline(9999);
    sp3_weekday = serial_port.readline(9999);
    sp3_modus = serial_port.readline(9999);
    sp3_alarm_enable = serial_port.readline(9999);
    sp3_alarm_mode = serial_port.readline(9999);
    sp3_alarm_hour = serial_port.readline(9999);
    sp3_alarm_min = serial_port.readline(9999);
    sp3_alarm_day = serial_port.readline(9999);
    sp3_alarm_month = serial_port.readline(9999);
    sp3_alarm_weekday = serial_port.readline(9999);
    sp3_alarmPoweroff = serial_port.readline(9999);
    sp3_alarm_hour_off = serial_port.readline(9999);
    sp3_alarm_min_off = serial_port.readline(9999);
    sp3_shutdown_enable = serial_port.readline(9999);
    sp3_shutdown_time = serial_port.readline(9999);
    sp3_warning_enable = serial_port.readline(9999);
    sp3_serialLessMode = serial_port.readline(9999);
    sp3_intervalAlarm = serial_port.readline(9999);
    sp3_intervalAlarmOnTime = serial_port.readline(9999);
    sp3_intervalAlarmOffTime = serial_port.readline(9999);
    sp3_batLevel_shutdown = serial_port.readline(9999);
    sp3_batLevel = serial_port.readline(9999);
    sp3_charging = serial_port.readline(9999);
    sp3_powerOnButton_enable = serial_port.readline(9999);
    sp3_powerOnButton_time = serial_port.readline(9999);
    sp3_powersave_enable = serial_port.readline(9999);
    sp3_poweroffMode = serial_port.readline(9999);
    sp3_poweroff_time_enable = serial_port.readline(9999);
    sp3_poweroff_time = serial_port.readline(9999);
    sp3_wakeupweekend_enable = serial_port.readline(9999);
    sp3_ADC_Wide = float(serial_port.readline(9999))/1000;
    sp3_ADC_BAT = float(serial_port.readline(9999))/1000;
    sp3_ADC_USB = float(serial_port.readline(9999))/1000;
    sp3_ADC_OUTPUT = float(serial_port.readline(9999))/1000;
    sp3_output_status = serial_port.readline(9999);
    sp3_powerfailure_counter = serial_port.readline(9999);
    sp3_firmwareVersion = serial_port.readline(9999);
    powerofftime_enabletest = (str(sp3_poweroff_time_enable, 'utf-8').rstrip('\n').zfill(2))

    date = int(sp3_date)

    strompi_year = int(sp3_date) // 10000
    strompi_month = int(sp3_date) % 10000 // 100
    strompi_day = int(sp3_date) % 100

    strompi_hour = int(sp3_time) // 10000
    strompi_min = int(sp3_time) % 10000 // 100
    strompi_sec = int(sp3_time) % 100

    if sp3_ADC_Wide > wide_range_volt_min:
        wide_range_volt = str(sp3_ADC_Wide) + 'V'
    else:
        wide_range_volt = ' not connected'

    if sp3_ADC_BAT > battery_volt_min:
        battery_volt = str(sp3_ADC_BAT) + 'V' + batterylevel_converter(int(sp3_batLevel),int(sp3_charging))
    else:
        battery_volt = ' not connected'

    if sp3_ADC_USB > mUSB_volt_min:
        microUSB_volt = str(sp3_ADC_USB) + 'V'
    else:
        microUSB_volt = ' not connected'

    output_volt = str(sp3_ADC_OUTPUT) + 'V'

    print(' ')
    print('---------------------------------')
    print('StromPi-Status:')
    print('---------------------------------')
    print('Time: ' + str(strompi_hour).zfill(2) + ':' + str(strompi_min).zfill(2) + ':' + str(strompi_sec).zfill(2))
    print('Date: ' + weekday_converter(int(sp3_weekday)) + ' ' + str(strompi_day).zfill(2) + '.' + str(strompi_month).zfill(2) + '.' + str(strompi_year).zfill(2))
    print(' ')
    print('StromPi-Output: ' + output_status_converter((int(sp3_output_status))))
    print(' ')
    print('StromPi-Mode: ' + strompi_mode_converter((int(sp3_modus))))
    print(' ')
    print('Raspberry Pi Shutdown: ' + enabled_disabled_converter(int(sp3_shutdown_enable)))
    print(' Shutdown-Timer: ' + str(sp3_shutdown_time, 'utf-8').rstrip('\n').zfill(2) + ' seconds')
    print(' ')
    print('Powerfail Warning: ' + enabled_disabled_converter(int(sp3_warning_enable)))
    print(' ')
    print('Serial-Less Mode: ' + enabled_disabled_converter(int(sp3_serialLessMode)))
    print(' ')
    print('Power Save Mode: ' + enabled_disabled_converter(int(sp3_powersave_enable)))
    print(' ')
    print('PowerOn-Button: ' + enabled_disabled_converter(int(sp3_powerOnButton_enable)))
    print(' PowerOn-Button-Timer: ' + str(sp3_powerOnButton_time, 'utf-8').rstrip('\n').zfill(2) + ' seconds')
    print(' ')
    print('Poweroff Mode: ' + enabled_disabled_converter(int(sp3_poweroffMode)))
    print(' ')
    print('Battery-Level Shutdown: ' + batterylevel_shutdown_converter(int(sp3_batLevel_shutdown)))
    print(' ')
    print('Powerfail-Counter: ' + str(sp3_powerfailure_counter, 'utf-8').rstrip('\n'))
    print(' ')
    print('---------------------------------')
    print('Alarm-Configuration:')
    print('---------------------------------')
    print('WakeUp-Alarm: ' + enabled_disabled_converter(int(sp3_alarm_enable)))
    if powerofftime_enabletest == "01":
        print(' Alarm-Mode: Wakeup Timer')
    else:
        print(' Alarm-Mode: ' + alarm_mode_converter(int(sp3_alarm_mode)))
    print(' Alarm-Time: ' + str(sp3_alarm_hour, 'utf-8').rstrip('\n').zfill(2) + ':' + str(sp3_alarm_min, 'utf-8').rstrip('\n').zfill(2))
    print(' Alarm-Date: ' + str(sp3_alarm_day, 'utf-8').rstrip('\n').zfill(2) + '.' + str(sp3_alarm_month, 'utf-8').rstrip('\n').zfill(2))
    print(' WakeUp-Alarm: ' + weekday_converter(int(sp3_alarm_weekday)))
    print(' ')
    print('PowerOff-Alarm: ' + enabled_disabled_converter(int(sp3_alarmPoweroff)))
    print(' PowerOff-Alarm-Time: ' + str(sp3_alarm_hour_off, 'utf-8').rstrip('\n').zfill(2) + ':' + str(sp3_alarm_min_off, 'utf-8').rstrip('\n').zfill(2))
    print(' ')
    print('Interval-Alarm: ' + enabled_disabled_converter(int(sp3_intervalAlarm)))
    print(' Interval-On-Time: ' + str(sp3_intervalAlarmOnTime, 'utf-8').rstrip('\n').zfill(2) + ' minutes')
    print(' Interval-Off-Time: ' + str(sp3_intervalAlarmOffTime, 'utf-8').rstrip('\n').zfill(2) + ' minutes')
    print(' ')
    print('---------------------------------')
    print('Voltage-Levels:')
    print('---------------------------------')
    print('Wide-Range-Inputvoltage: ' + wide_range_volt)
    print('LifePo4-Batteryvoltage: ' + battery_volt)
    print('microUSB-Inputvoltage: ' + microUSB_volt)
    print('Output-Voltage: ' + output_volt)
    print(' ')

except KeyboardInterrupt:
    print('interrupted!')

serial_port.close()