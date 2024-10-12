import subprocess
import sys


obs_dir = "../../../observations/network/"
BS = ["4","8","16","32","64","256","512","1024"]
NP = [1, 2, 3, 4, 5, 6, 7, 8]
NP = [1]
BS = ["8"]

test = sys.argv[1]
for i in BS:
    for j in NP:
        with open(obs_dir+"{}_tcpbw_S{}_{}".format(test,j,i),"w") as f:
            subprocess.run("./tcp_bw.sh {} {}".format(j,i), shell=True, stdout=f)
