#Continue configuration from RQ1
curl "http://172.16.137.2:8080/poll?poll=40"
../../../setup/rps.sh 0
sudo ethtool -K ens4np0 ntuple off

sudo nvme disconnect -d /dev/nvme0
../../../setup/nvmeof_tcp_initiator_setup.sh thesis.dev0 10 10
sudo nvme disconnect -d /dev/nvme1
../../../setup/nvmeof_tcp_initiator_setup.sh thesis.dev1 10 10


export FDEVICE="/dev/nvme0n1"
export BDEVICE="/dev/nvme1n1"
export MAX_IOPS=180 #Saturation point of the resoource in KIOPS

curl http://172.16.137.2:8080/rss?count=1
python3 fio_runner.py remote_ID_TS_SD_split_bread_fread
curl http://172.16.137.2:8080/rss?count=10
