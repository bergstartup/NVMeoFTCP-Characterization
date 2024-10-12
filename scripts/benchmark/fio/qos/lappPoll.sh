DEVICE=nvme0c0n1
curl "http://127.0.0.1:8080/sched?sched=none&dev=${DEVICE}"
python3 fio_runner.py remote_poll_bread_fread
