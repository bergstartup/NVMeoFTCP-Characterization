curl "http://$1:8080/poll?poll=0"
sudo nvme disconnect -d /dev/nvme0
../../../setup/nvmeof_tcp_initiator_setup.sh thesis.dev0 10 0
sudo python3 fio_runner.py remote_perf_npoll

sudo nvme disconnect -d /dev/nvme0
../../../setup/nvmeof_tcp_initiator_setup.sh thesis.dev0 10 10
sudo python3 fio_runner.py remote_perf_poll
