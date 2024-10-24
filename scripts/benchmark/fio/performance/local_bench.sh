sudo nvme disconnect -d /dev/nvme0

#Number of I/O polling queues based on Experiment
../../../setup/nvmeof_tcp_initiator_setup.sh thesis.dev0 10 10

#Setting target polling
curl "http://localhost:8080/poll?poll=40"

#Disabline arfs
../../../setup/rps.sh 0
sudo ethtool -K ens4np0 ntuple off

python3 fio_runner.py local_bench
