import os
import sys
import json

obs_dir="../../../observations/network/"
files = os.listdir(obs_dir)

crunched_numbers = {}
for i in files:
    if "crunched" in i:
        continue
    try:
        with open(obs_dir+i,"r") as fp:
            d = json.load(fp)
            bw =  d["end"]["sum_sent"]["bits_per_second"]
            #mbps to GBps
            bw = bw/(8*(1024**3))
            
            cwnd = 0
            all_streams = d["end"]["streams"]
            for j in all_streams:
                cwnd += j["sender"]["max_snd_cwnd"]
            cwnd /= len(all_streams)

            retransmits = d["end"]["sum_sent"]["retransmits"]

            crunched_numbers[i] = {"bw":bw,"rt":retransmits,"avg_win":cwnd}
    except Exception as e:
        print(i, e)

with open(obs_dir+"crunched_numbers.json","w") as fp:
    json.dump(crunched_numbers, fp)
