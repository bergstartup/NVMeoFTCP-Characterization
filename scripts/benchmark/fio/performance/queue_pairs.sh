sudo nvme disconnect -d /dev/nvme0
../../../setup/nvmeof_tcp_initiator_setup.sh thesis.dev0 1 0
sudo python3 fio_runner.py remote_1qp_npoll
sudo nvme disconnect -d /dev/nvme0
../../../setup/nvmeof_tcp_initiator_setup.sh thesis.dev0 2 0
sudo python3 fio_runner.py remote_2qp_npoll
sudo nvme disconnect -d /dev/nvme0
../../../setup/nvmeof_tcp_initiator_setup.sh thesis.dev0 4 0
sudo python3 fio_runner.py remote_4qp_npoll
sudo nvme disconnect -d /dev/nvme0
../../../setup/nvmeof_tcp_initiator_setup.sh thesis.dev0 8 0
sudo python3 fio_runner.py remote_8qp_npoll
sudo nvme disconnect -d /dev/nvme0
../../../setup/nvmeof_tcp_initiator_setup.sh thesis.dev0 10 0
sudo python3 fio_runner.py remote_10qp_npoll
sudo nvme disconnect -d /dev/nvme0
../../../setup/nvmeof_tcp_initiator_setup.sh thesis.dev0 12 0
sudo python3 fio_runner.py remote_12qp_npoll

#Set back to normal
sudo nvme disconnect -d /dev/nvme0
../../../setup/nvmeof_tcp_initiator_setup.sh thesis.dev0 10 0
