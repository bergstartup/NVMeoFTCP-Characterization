import sys
import json
import os

#Observation directory
observation_dir = "../../../../observations/performance_limit/"
cpu_util_dir = "../../../monitor/"

#Define workload parameters
workload_type = ["read","write","randread","randwrite"]

queue_depth = [1, 32, 64, 128]

number_of_process = [1, 2, 4, 8]

devices = ["RAM", "SSD"]

def get_cpu_avg(exp):
    util = {}
    with open(cpu_util_dir+exp,"r") as f:
        lines = f.readlines()[-18:]
        if "iowait" not in lines[0]:
            lines = lines[-11:]
        else:
            lines = lines[-17:]

        for line in lines:
            obs = line.split()
            cpu = obs[1]
            user = obs[2]
            sys = obs[4]
            iowait = obs[5]
            util[cpu] = {"usr":user,"sys":sys,"io":iowait}
    return util

def list_all_experiments(node):
    experiments = []
    #TODO: Change the order accordingly!
    for dt in devices:
        for wt in workload_type:
            for qd in queue_depth:
                for np in number_of_process:
                    parameters = {}
                    #parameters["DEVICE"] = devices[dt]
                    parameters["WORKLOAD"] = wt
                    if "read" in wt:
                        parameters["TYPE"] = "read"
                    else:
                        parameters["TYPE"] = "write"
                    parameters["QD"] = qd
                    parameters["NPROCESS"] = np
                    parameters["NAME"] = node+"_"+dt+"_"+wt+"_"+"QD"+str(qd)+"_"+"P"+str(np)
                    experiments.append(parameters)
    
    return experiments


def get_experiment(node, dt, wt, qd, np):
    return node+"_"+dt+"_"+wt+"_"+"QD"+str(qd)+"_"+"P"+str(np)




#Crunch all observations
all_observations = {}

try:
    with open(observation_dir+'crunched_numbers_performace_limit.json','r') as f:
        all_observations = json.load(f)
except:
    pass


experiments = os.listdir(observation_dir)
#experiments = ["remote_npoll_iou_SSD_randread_QD64_P1_4k"]
for exp in experiments:
    if "bpf" in exp or "crunched_numbers_performance_limit.json" in exp:
        continue

    try:
        with open(observation_dir+exp,'r') as f:
            data = json.load(f)
            
            #latency
            operation = "read"
            if "write" in exp:
                operation = "write"
            obs = data['jobs'][0][operation]
            obs_dict = {}
            obs_dict['latency'] = obs['clat_ns']
            obs_dict['iops'] = {'min':obs['iops_min'],'max':obs['iops_max'],'mean':obs['iops_mean'],'stddev':obs['iops_stddev'],'N':obs['iops_samples']}
            obs_dict['bw'] = {'min':obs['bw_min'],'max':obs['bw_max'],'mean':obs['bw_mean'],'stddev':obs['bw_dev'],'N':obs['bw_samples']}
            obs_dict['fio_cpu'] = {'runtime':data['jobs'][0]['job_runtime'],'usr':data['jobs'][0]['usr_cpu'],'sys':data['jobs'][0]['sys_cpu'],'ctx':data['jobs'][0]['ctx']}
            if "local" not in exp:
                initiator_cpu = get_cpu_avg(exp+"_initiator_cpu")
                target_cpu = get_cpu_avg(exp+"_target_cpu")
                obs_dict['init_cpu'] = initiator_cpu
                obs_dict['target_cpu'] = target_cpu
            else:
                local_cpu = get_cpu_avg(exp+"_local_cpu")
                obs_dict['local_cpu'] = local_cpu
            all_observations[exp.split(".")[0]] = obs_dict
    except Exception as e:
        print(exp, e)



with open(observation_dir+'crunched_numbers_performance_limit.json','w') as f:
    json.dump(all_observations, f)
