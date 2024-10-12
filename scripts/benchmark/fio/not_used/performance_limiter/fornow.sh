


# Array of values
values=(1 2 4 8 10)
sudo nvme disconnect -d /dev/nvme0
# Iterate over each value
for value in "${values[@]}"
do
	cd /home/user/master-thesis/scripts/setup
	sudo ./nvmeof_tcp_initiator_setup.sh $value 0
	cd /home/user/master-thesis/scripts/benchmark/fio/performance
	sudo -E python3 fio_runner.py "remote_${value}c_npoll"
	sudo nvme disconnect -d /dev/nvme0
done
