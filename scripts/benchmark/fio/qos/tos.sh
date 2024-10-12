#sudo nvme disconnect -d /dev/nvme0
#sudo nvme disconnect -d /dev/nvme1

#Execute queue pair bpf trace
#curl http://127.0.0.1:8080/bpf?script=nvmeof_queue_pairs.bt?id=queue_pairs
#Connect for device 0 with tos 0x10 (used for L-app)
#../../../setup/
#Stop the queue pair bpf trace
#Set the ports to queue 0 in the target

#Do the above steps for device 1
#Connect to device 1 with tos 0x8 (used for T-app)
#Assign ports to queues 1-9 in the target


#Execute with best nice value observed from the prev experiment

python3 fio_runner.py remote_IS_TD_SD_baseline_tos_bread_fread
#python3 fio_runner.py remote_IS_TD_SD_nice5_tos_bread_fread
#python3 fio_runner.py remote_IS_TD_SD_nice10_tos_bread_fread
#python3 fio_runner.py remote_IS_TD_SD_nice15_tos_bread_fread
#python3 fio_runner.py remote_IS_TD_SD_nice19_tos_bread_fread
