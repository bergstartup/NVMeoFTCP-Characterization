#provide ip addr and port of target as cmd line arg
sudo modprobe nvme
sudo modprobe nvme-tcp
sudo modprobe nvme-fabrics
sudo nvme connect -t tcp -n $1 -a 172.16.137.2 -s 4420 -i $2 -P $3 #-T $4
