Monitoring tool of /proc/diskstats
=================================
The tool has is sole purpose of parsing /proc/diskstats and store it as csv files for later parsing.

## Usage
```
python diskstats.py -h
usage: diskstats.py [-h] [-l sleep] [-d name [name ...]]

Parser tool for /proc/diskstats

optional arguments:
  -h, --help            show this help message and exit
  -l sleep, --loop sleep
                        Runs the program in a loop. Takes the looptime as
                        option.
  -d name [name ...], --device name [name ...]
                        Names, like sda, sda1...
```

## Descriptions of fields in /proc/diskstats
    The /proc/diskstats file displays the I/O statistics
    of block devices. Each line contains the following 14
    fields:
        1 - major number
        2 - minor mumber
        3 - device name
        4 - reads completed successfully
        5 - reads merged
        6 - sectors read
        7 - time spent reading (ms)
        8 - writes completed
        9 - writes merged
       10 - sectors written
       11 - time spent writing (ms)
       12 - I/Os currently in progress
       13 - time spent doing I/Os (ms)
       14 - weighted time spent doing I/Os (ms)
        For more details refer to Documentation/iostats.txt
