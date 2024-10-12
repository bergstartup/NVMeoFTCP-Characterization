import sys
import json
import os

#Observation directory
observation_dir = "../../../../observations/performance/"
cpu_util_dir = "../../../monitor/"
RUNS = 1



def reduce(dicts):
    def recurse(keys, aggregated_data):
        for k, v in keys.items():
            if isinstance(v, dict):
                # Recur for dictionaries
                aggregated_data.setdefault(k, {})
                recurse(v, aggregated_data[k])
            else:
                # Aggregate numeric values
                if k not in aggregated_data:
                    aggregated_data[k] = 0
                    #aggregated_data[k] = []
                aggregated_data[k] += v
                #aggregated_data[k].append(v)

    # Create an empty dictionary to hold aggregated results
    aggregated_data = {}
    
    # Count the number of runs
    num_runs = len(dicts)
    
    # Aggregate the data from each run
    for run_key, run_data in dicts.items():
        recurse(run_data, aggregated_data)

    # Calculate the average
    def calculate_average(data):
        for k, v in data.items():
            if isinstance(v, dict):
                calculate_average(v)
            else:
                #v.sort()
                #data[k] = v[RUNS//2]
                data[k] = v / num_runs
    
    calculate_average(aggregated_data)
    return aggregated_data



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

def parse(exp):
    obs_dict = {}
    with open(observation_dir+exp,'r') as f:
        data = json.load(f)
        
        #latency
        obs = data['jobs'][0]["read"]
        obs_dict['latency'] = obs['clat_ns']
        obs_dict['iops'] = {'min':obs['iops_min'],'max':obs['iops_max'],'mean':obs['iops_mean'],'stddev':obs['iops_stddev'],'N':obs['iops_samples']}
        obs_dict['bw'] = {'min':obs['bw_min'],'max':obs['bw_max'],'mean':obs['bw_mean'],'stddev':obs['bw_dev'],'N':obs['bw_samples']}
        obs_dict['fio_cpu'] = {'runtime':data['jobs'][0]['job_runtime'],'usr':data['jobs'][0]['usr_cpu'],'sys':data['jobs'][0]['sys_cpu'],'ctx':data['jobs'][0]['ctx']}
        try:
            #Handle if no CPU usage is present
            if "local" not in exp:
                initiator_cpu = get_cpu_avg(exp+"_initiator_cpu")
                target_cpu = get_cpu_avg(exp+"_target_cpu")
                obs_dict['init_cpu'] = initiator_cpu
                obs_dict['target_cpu'] = target_cpu
            else:
                local_cpu = get_cpu_avg(exp+"_local_cpu")
                obs_dict['local_cpu'] = local_cpu
        except:
            pass
        #runs_dict[exp.split(".")[0]] = obs_dict
    return obs_dict

#Crunch all observations
all_observations = {}
with open(observation_dir+'crunched_numbers_performance.json','r') as f:
    all_observations = json.load(f)
    
experiments = os.listdir(observation_dir)
#experiments = ["remote_npoll_iou_SSD_randread_QD64_P1_4k"]
for exp in experiments:
    if "bpf" in exp or "crunched_numbers_performance.json" in exp:
        continue
    if "RUN0" not in exp:
        continue
    try:
        runs_dict = {}
        for i in ["RUN{}".format(j) for j in range(RUNS)]:
            runs_dict[i] = parse(exp[:-4]+i) 
        op = reduce(runs_dict)
        all_observations[exp[:-5]] = op
    except Exception as e:
        print(exp, e)



with open(observation_dir+'crunched_numbers_performance.json','w') as f:
    json.dump(all_observations, f)
