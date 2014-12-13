#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
import os, re, csv
import argparse
from time import sleep

# Tool for getting /proc/diskstats
DISKSTATS_PATH = '/proc/diskstats'
HEADERS = ['major_number', 'minor_number', 'device_name', 'read_completed_successfully',
        'reads_merged', 'sectors_read', 'time_spent_reading(ms)', 'writes_completed',
        'writes_merged', 'sectors_written', 'time_spent_writing_(ms)', 'IO_currently_in_progress',
        'time_spent_doing_IO_(ms)', 'weighted_time_spent_doing_IO']

lastread_timestamp = None

def read_diskstats():
    global lastread_timestamp
    devs = []
    with open(DISKSTATS_PATH, 'r') as f:
        for line in f.readlines():
            # check if line is disk
            devs.append(dict(zip(HEADERS, re.split('\s+', line.strip()))))
    lastread_timestamp = datetime.now()

    return devs

def find_device(data, device):
    return (item for item in data if item['device_name'] == device).next()

def write_diskstats(data, device=None):
    global lastread_timestamp
    csv_data = []

    if device:
        if len(device) > 1:
            filename = "mon_diskstats_{}".format("_".join(device))
            if not os.path.isfile(filename):
                csv_data = [HEADERS]
            d = []
            for dev in device:
                d.append(find_device(data, dev))

            if len(d) < 1:
                print "No devices found by filter {}".format(" ".join(device))
                return False
            else:
                data = d

                for dev in data:
                    tmp = [dev[h] for h in HEADERS]
                    tmp.insert(0, lastread_timestamp.isoformat())
                    csv_data.append(tmp)



        else:
            data = find_device(data, device[0])
            filename = "mon_{}".format(device[0].strip())
            if not os.path.isfile(filename):
                csv_data = [HEADERS]
            tmp = [data[h] for h in HEADERS]
            tmp.insert(0, lastread_timestamp.isoformat())
            csv_data.append(tmp)

    else:
        filename = "mon_diskstats"
        if not os.path.isfile(filename):
            csv_data = [HEADERS]
        for dev in data:
            tmp = [dev[h] for h in HEADERS]
            tmp.insert(0, lastread_timestamp.isoformat())
            csv_data.append(tmp)

    with open(filename, 'a') as f:
        w = csv.DictWriter(f, HEADERS)
        w.writer.writerows(csv_data)

def gather_and_write(devices):
    data = read_diskstats()
    write_diskstats(data, devices)
    return data

def main():
    parser = argparse.ArgumentParser(description='Parser tool for /proc/diskstats')
    parser.add_argument('-l', '--loop', type=int, metavar='sleep',
            help='Runs the program in a loop. Takes the looptime as option.')
    parser.add_argument('-d', '--device', metavar='name', nargs='+', default=None, help='Names, like sda, sda1...')
    args = parser.parse_args()

    try:
        if args.loop:
            while True:
                print "Running..."
                data = gather_and_write(args.device)
                sleep(args.loop)
        else:
            data = gather_and_write(args.device)
            print find_device(data, 'vda')
    except KeyboardInterrupt:
        print "Aborting..."

if __name__ == '__main__':
    main()
