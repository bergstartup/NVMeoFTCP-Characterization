sudo nvme disconnect -d /dev/nvme0
../../../setup/nvmeof_tcp_initiator_setup.sh thesis.dev0 10 10
curl "http://172.16.137.2:8080/poll?poll=0"
python3 fio_runner.py remote_tpoll0
curl "http://172.16.137.2:8080/poll?poll=50"
python3 fio_runner.py remote_tpoll50
curl "http://172.16.137.2:8080/poll?poll=100"
python3 fio_runner.py remote_tpoll100
