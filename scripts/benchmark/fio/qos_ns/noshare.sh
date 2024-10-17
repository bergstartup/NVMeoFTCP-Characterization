#!/bin/sh

#Continue configuration from RQ1
curl "http://172.16.137.2:8080/poll?poll=10"
../../../setup/rps.sh 0
sudo ethtool -K ens4np0 ntuple off


#Regarding QOS
#ID referes to initiator core isolated (split)



#TD refers to target core isolated (Make sure set flow steering in the target)
#LDEVICE
sudo nvme disconnect -d /dev/nvme0
sudo ../../../bpf/nvmeof_queue_pairs.bt > op &
bpfpid=$!
sleep 5
../../../setup/nvmeof_tcp_initiator_setup.sh thesis.dev0 10 10
kill -9 $bpfpid

grep port op | awk '{print $NF}' > ports
rm op

line_number=1
q=0
while read -r port; do
	id=$line_number
	curl "http://172.16.137.2:8080/fctrl?port=$port&id=$id&q=$q"
	line_number=$(expr $line_number + 1)
done < ports



#TDEVICE
sudo nvme disconnect -d /dev/nvme1
sudo ../../../bpf/nvmeof_queue_pairs.bt > op &
bpfpid=$!
sleep 5
../../../setup/nvmeof_tcp_initiator_setup.sh thesis.dev1 10 10
kill -9 $bpfpid

grep port op | awk '{print $NF}' > ports
rm op

line_number=22
q=1
while read -r port; do
        id=$line_number
        curl "http://172.16.137.2:8080/fctrl?port=$port&id=$id&q=$q"
        q=$(( (q % 9) + 1 ))
	line_number=$(expr $line_number + 1)
done < ports
rm ports


#SD refers to SSD isolated (Use different SSD)
export FDEVICE=/dev/nvme0n1
export BDEVICE=/dev/nvme1n1
export MAX_IOPS=450 
python3 fio_runner.py remote_ID_TD_SD_baseline_bread_fread


#Remove flow control in target
lines=43
curl "http://172.16.137.2:8080/remfctrl?total=$lines"
