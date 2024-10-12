sudo nvme disconnect -d /dev/nvme0
../../../setup/nvmeof_tcp_initiator_setup.sh thesis.dev0 10 10
curl "http://172.16.137.2:8080/poll?poll=100"

#Without arfs
../../../setup/rps.sh 0
sudo ethtool -K ens4np0 ntuple off
sudo python3 fio_runner.py remote_perf_woarfs

#With arfs
../../../setup/rps.sh 32768
sudo ethtool -K ens4np0 ntuple on
sudo python3 fio_runner.py remote_perf_arfs
