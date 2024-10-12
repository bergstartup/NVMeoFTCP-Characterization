#Include backgroud flow
#-b for 4KB block size 14Gbps
#-b for 64KB bs is 13.68Gbps
taskset -c 1-9 iperf3 -c 172.16.137.2 -t 200 -R -P $1 -b $(echo "scale=2; $2 / $1" | bc)G -l $3 > /dev/null &

pid=$!
echo "BG flow count $1"

netperf -T 0,0 -l 180 -s 10 -t TCP_RR -H 172.16.137.2 -- -r 72,4KB -O max_latency,p99_latency,stddev_latency

kill -9 $pid
wait $pid
