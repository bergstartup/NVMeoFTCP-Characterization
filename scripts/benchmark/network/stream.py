import subprocess

obs_dir = "../../../observations/network/"
BS = ["4","8","16","32","64","128", "256", "512"]
NP = [1, 2, 3, 4, 5, 6, 7, 8]

for i in BS:
    for j in NP:
        subprocess.run("./tcp_stream.sh {} {} {}tcpbw_S{}_{}".format(j,i,obs_dir,j,i), shell=True, stdout=None)
