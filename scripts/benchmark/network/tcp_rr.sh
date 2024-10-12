for i in 4 8 16 32 64 128 256 512
do
	netperf -t TCP_RR -H 172.16.137.2 -P 0 -B "For size $i KB" -- -r 72,${i}KB -O mean_latency
done
