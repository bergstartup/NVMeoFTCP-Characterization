#Include backgroud flow
taskset -c "1-9" iperf3 -c 172.16.137.2 --tos 8 -t 65 -R -P $1 -l 64KB > /dev/null &

pid=$!
echo "BG flow count $1"

taskset -c 0 netperf -Y 10 -l 60 -t TCP_RR -H 172.16.137.2 -P 0 -B "FR flow (Interference NP $1)" -- -r 72,4KB -O mean_latency

kill -9 $pid
