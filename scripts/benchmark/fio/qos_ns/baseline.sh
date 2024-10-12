#IS referes to initiator core isolated
#TD refers to target core isolated
#SD refers to SSD isolated
curl "http://172.16.137.2:8080/sched?sched=none&dev=nvme0n1"
curl "http://172.16.137.2:8080/sched?sched=none&dev=nvme1n1"
curl "http://172.16.137.2:8080/sched?sched=none&dev=nvme2n1"
python3 fio_runner.py remote_ID_TD_SD_split_bread_fread
