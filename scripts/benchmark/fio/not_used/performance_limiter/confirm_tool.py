import os
from random import sample
import math


confidence_string = """
0.70	1.04
0.75	1.15
0.80	1.28
0.85	1.44
0.90	 1.645
0.92	1.75
0.95	1.96
0.96	2.05
0.98	2.33
0.99	2.58
"""
confidence = {float(i.split("\t")[0]):float(i.split("\t")[1]) for i in confidence_string.split("\n")[1:11]}

def get_obs_from_log(log_file):
    observations = []
    with open(log_file,'r') as f:
        lines = f.readlines()
        prev_ts=0
        obs = []
        for line in lines:
            ts = int(line.split(",")[0])
            if ts < prev_ts:
                observations.append(obs)
                obs = []
            prev_ts = ts
            val = line.split(",")[1]
            obs.append(float(val))

        observations.append(obs)
    return observations

def get_ahal(subset,z_score):
    n = len(subset)
    al = math.floor((n-z_score * (n ** 0.5)) / 2)
    ah = 1 + math.ceil((n+z_score * (n ** 0.5)) / 2)
    
    if al - 1 == -1:
        al = 1

    if ah > len(subset):
        ah = len(subset)

    return subset[al-1], subset[ah-1]

def apply_confirm(observations, confidence_level, eb):
    #Select initial subset size
    #Iterate from initial subset size to observation size
        #Select N random subsets from the observations
        #Get mean of (median, eh, el (median * z_score), ah, al (observation[index] -> index from confidence level) of subset) of all subsets
        #if [al, ah] is within [el, eh] then return true
    init_subset_size = 10
    subset_sampling = 20
    z_score = confidence[confidence_level]
    for subset_size in range(init_subset_size, len(observations)+1):
        median, el, eh, al, ah = [0 for i in range(5)]
        for subset in range(subset_sampling):
            sam = sample(observations,subset_size)
            sam.sort()
            #Median
            index = math.floor(len(sam)*0.5)
            median += sam[index]
            sal,sah = get_ahal(sam, z_score)
            al += sal
            ah += sah

        avg_median, avg_al, avg_ah = [i/subset_sampling for i in [median, al, ah]]
        avg_el, avg_eh = [avg_median - (avg_median * eb), avg_median + (avg_median * eb)]
        #print(subset_size, avg_median, avg_el, avg_eh, avg_al, avg_ah)
        if(avg_al>avg_el) and (avg_ah<avg_eh):
            return True

    return False



"""
logs = os.listdir("logs/")
#observations = [float(i) for i in ['12.540307', '12.537640', '12.893903', '12.450946', '12.500611', '12.793001', '12.467446', '12.567436', '12.353851', '13.023272', '12.540307', '12.537640', '12.893903', '12.450946', '12.500611', '12.793001', '12.467446', '12.567436', '12.353851', '13.023272', '12.540307', '12.537640', '12.893903', '12.450946', '12.500611', '12.793001', '12.467446', '12.567436', '12.353851', '13.023272']]
#observations = [float(i) for i in  ['12.540307', '12.537640', '12.893903', '12.450946', '12.500611', '12.793001', '12.467446', '12.567436', '12.353851', '13.023272', '12.540307', '12.537640', '12.893903', '12.450946', '12.500611', '12.793001', '12.467446', '12.567436', '12.353851', '13.023272', '12.540307', '12.537640', '12.893903']]
#print(apply_confirm(observations, 0.95, 0.05))

for log in logs:
    observations = get_obs_from_log("./logs/"+log)
    if len(observations) == 0:
        print("No observations : ", log)
        continue
    accept = apply_confirm(observations, 0.95, 0.05)
    if not accept:
        print("Not accept : ", log)
    else:
        print("Accept : ", log)
"""
