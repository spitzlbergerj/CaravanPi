# CaravanPi
System for measuring and displaying various values in caravans and motor homes, including climate values, filling levels and levelling data. Magic Mirror is used for presentation.

# .crontabs
In order to automatically determine and store the measurement data, a series of scripts must be started when the Raspberry Pi is started. I use the Crontabs. 

Alternatively the scripts can be started via pm2, which is installed anyway due to the Magic Mirror.

## crontab of user root
The crontab of the root user is used to start the backup timer and after booting and to start Logrotate timer and after booting.

Time control and after booting, because the Pi may not always be running.

## crontab of user pi
Via the crontab of the user pi all sensors are queried regularly. Currently the following sensors are read by Python script:

- Temperature Sensor
- Climate Sensor
- gas cylinder scale
- position sensor

Finally, Logrotate is executed via this crontab. Time-controlled and when starting the Pi