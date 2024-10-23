#Disconnect from the device
sudo nvme disconnect -d /dev/nvme0

#Set polling
../../../setup/nvmeof_tcp_initiator_setup.sh thesis.dev0 10 10

#Without arfs
../../../setup/rps.sh 0
sudo ethtool -K $2 ntuple off 

curl "http://$1:8080/poll?poll=0"
python3 fio_runner.py remote_tpoll0
curl "http://$1:8080/poll?poll=10"
python3 fio_runner.py remote_tpoll10
curl "http://$1:8080/poll?poll=20"
python3 fio_runner.py remote_tpoll20
curl "http://$1:8080/poll?poll=40"
python3 fio_runner.py remote_tpoll40
curl "http://$1:8080/poll?poll=80"
python3 fio_runner.py remote_tpoll80
curl "http://$1:8080/poll?poll=160"
python3 fio_runner.py remote_tpoll160

