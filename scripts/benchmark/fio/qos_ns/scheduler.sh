curl "http://172.16.137.2:8080/sched?sched=kyber&dev=nvme1n1"
curl "http://172.16.137.2:8080/sched?sched=kyber&dev=nvme2n1"
python3 fio_runner.py remote_ID_TD_SD_tkyber_bread_fread
