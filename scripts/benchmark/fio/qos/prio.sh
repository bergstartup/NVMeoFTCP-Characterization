DEVICE=nvme0c0n1
curl "http://127.0.0.1:8080/sched?sched=mq-deadline&dev=${DEVICE}"
python3 fio_runner.py remote_pollprio_bread_fread
