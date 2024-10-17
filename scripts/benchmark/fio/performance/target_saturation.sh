#Disconnect from the device
sudo nvme disconnect -d /dev/nvme0

#Set polling
../../../setup/nvmeof_tcp_initiator_setup.sh thesis.dev0 10 10

#Without arfs
../../../setup/rps.sh 0
sudo ethtool -K ens4np0 ntuple off 

#Do experiments
curl http://172.16.137.2:8080/rss?count=1
sudo python3 fio_runner.py remote_target_C1
curl http://172.16.137.2:8080/rss?count=2
sudo python3 fio_runner.py remote_target_C2
curl http://172.16.137.2:8080/rss?count=3
sudo python3 fio_runner.py remote_target_C3
curl http://172.16.137.2:8080/rss?count=10
