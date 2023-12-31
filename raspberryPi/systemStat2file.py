#!/usr/bin/python3
# coding=utf-8
# systemStat2file.py
#
# zyklische Abfrage einiger Systemwerte
# Intervall 5 Minuten (oder laut Parameter)
# Bei CPU Temperaturen über 75°C wird das Intervall auf 30 Sekunden verkürzt
#
# Aufruf-Parameter
# systemStat2file.py -f
# 	-h	display guide 
# 	-f	write values to file 
# 	-s	display values on screen 
#
# erzeugt mit Hilfe von ChatGPT 4
#-------------------------------------------------------------------------------

import os
import time
import sys
import argparse
import subprocess

def get_cpu_temperature():
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as file:
        temp = float(file.read()) / 1000
    return temp

def get_gpu_temperature():
    try:
        gpu_temp_output = subprocess.check_output(['/usr/bin/vcgencmd', 'measure_temp']).decode()
        gpu_temp = float(gpu_temp_output.split('=')[1].split("'")[0])
        return gpu_temp
    except Exception as e:
        print(f"Fehler beim Auslesen der GPU-Temperatur: {e}")
        return None

def get_cpu_usage():
    with open('/proc/stat', 'r') as f:
        lines = f.readlines()
    cpu_times = lines[0].split()[1:5]
    cpu_times = list(map(int, cpu_times))
    idle_time = cpu_times[3]
    total_time = sum(cpu_times)

    time.sleep(1)

    with open('/proc/stat', 'r') as f:
        lines = f.readlines()
    cpu_times_2 = lines[0].split()[1:5]
    cpu_times_2 = list(map(int, cpu_times_2))
    idle_time_2 = cpu_times_2[3]
    total_time_2 = sum(cpu_times_2)

    idle_delta = idle_time_2 - idle_time
    total_delta = total_time_2 - total_time

    cpu_usage = 100.0 * (1 - idle_delta / total_delta)
    return cpu_usage

def get_ram_usage():
    with open("/proc/meminfo", "r") as f:
        lines = f.readlines()
    total_memory = int(lines[0].split()[1])
    free_memory = int(lines[1].split()[1])
    used_memory = total_memory - free_memory
    return (used_memory / total_memory) * 100

def get_disk_usage():
    disk_usage = os.popen("df -h | awk '$NF==\"/\"{print $(NF-1)}'").readline().strip()
    return disk_usage

def get_network_traffic(interface='eth0'):
    net_stats = os.popen(f"cat /sys/class/net/{interface}/statistics/rx_bytes").readline().strip()
    net_stats_mb = int(net_stats) / (1024 ** 2)
    return net_stats_mb

def get_process_count():
    process_count = os.popen("ps -e | wc -l").readline().strip()
    return process_count

def get_system_uptime():
    with open("/proc/uptime", "r") as f:
        uptime_seconds = float(f.readline().split()[0])
    return uptime_seconds

def main():
    parser = argparse.ArgumentParser(description='Systemstatistiken überwachen')
    parser.add_argument('-i', '--interval', type=int, default=300,
                        help='Intervall in Sekunden für regelmäßige Abfragen (Standard: 300 Sekunden)')
    parser.add_argument('-s', '--screen', action='store_true',
                        help='Aktiviert die Ausgabe auf dem Bildschirm')
    parser.add_argument('-f', '--file', action='store_true',
                        help='(Abwärtskompatibilität) Keine Funktion')

    args = parser.parse_args()
    
    normal_interval = args.interval
    high_temp_interval = 30  # Abfrageintervall bei hoher Temperatur: 30 Sekunden
    interval = normal_interval

    try:
        while True:
            cpu_temp = get_cpu_temperature()
            gpu_temp = get_gpu_temperature()
            cpu_usage = get_cpu_usage()
            ram_usage = get_ram_usage()
            disk_usage = get_disk_usage()
            net_traffic = get_network_traffic()
            process_count = get_process_count()
            system_uptime = get_system_uptime()

            if args.screen:
                print(f"CPU-Temperatur: {cpu_temp:.2f}°C")
                print(f"GPU-Temperatur: {gpu_temp:.2f}°C")
                print(f"CPU-Auslastung: {cpu_usage:.2f}%")
                print(f"RAM-Auslastung: {ram_usage:.2f}%")
                print(f"Speicherplatz: {disk_usage}")
                print(f"Netzwerkauslastung: {net_traffic:.2f} MB")
                print(f"Anzahl laufender Prozesse: {process_count}")
                print(f"Systemlaufzeit: {system_uptime:.2f} Sekunden")

            # Anpassung des Intervalls basierend auf der CPU-Temperatur
            if cpu_temp > 75 and interval != high_temp_interval:
                interval = high_temp_interval
            elif cpu_temp <= 75 and interval != normal_interval:
                interval = normal_interval

            time.sleep(interval)
    except KeyboardInterrupt:
        if args.screen:
            print("\nProgramm wurde durch Benutzer unterbrochen. Beende...")
        sys.exit(0)

if __name__ == "__main__":
    main()
