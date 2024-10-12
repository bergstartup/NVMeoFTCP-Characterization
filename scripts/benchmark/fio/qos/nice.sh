#IS referes to initiator core sharing
#TD refers to target core isolated
#SD refers to SSD isolated
#the nice value specified here is the magnitued and will be used
#as negative values
python3 fio_runner.py remote_IS_TD_SD_nice5_bread_fread
python3 fio_runner.py remote_IS_TD_SD_nice10_bread_fread
python3 fio_runner.py remote_IS_TD_SD_nice15_bread_fread
python3 fio_runner.py remote_IS_TD_SD_nice19_bread_fread
