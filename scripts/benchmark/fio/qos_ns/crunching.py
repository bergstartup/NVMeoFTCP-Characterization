import sys
import copy
import os
import json
import re
import statistics



#Observation directory
observation_dir = "../../../../observations/qos2/"
monitor_dir = "../../../monitor/"
RUNS = 5
def init_reqprocessing(exp):
    obs_pattern = re.compile(r'@compute_mean\[(\d+)\]: (\d+)')
    #To avoid .json at the end
    fpath = monitor_dir+exp[:-5]+"_initiator_reqprocesstime"
    lowestPid = None
    val2ret = 0
    with open(fpath,'r') as f:
        for line in f:
            line = line.strip()
            match = obs_pattern.search(line)
            if match and ((lowestPid is None) or (lowestPid > int(match.group(1)))):
                lowestPid = int(match.group(1))
                val2ret = int(match.group(2))
    return val2ret


def target_blk(exp):
    obs_pattern = re.compile(r'@blk_mean\[(\d+)\]: (\d+)')
    #To avoid .json at the end
    fpath = monitor_dir+exp[:-5]+"_target_micro"
    with open(fpath,'r') as f:
        for line in f:
            line = line.strip()
            match = obs_pattern.search(line)
            #match = re.findall(obs_pattern, line)
            if match:
                clm3 = int(match.group(2))
                return clm3

    return 0

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
                    #aggregated_data[k] = 0
                    aggregated_data[k] = []
                #aggregated_data[k] += v
                aggregated_data[k].append(v)

    # Create an empty dictionary to hold aggregated results
    aggregated_data = {}
    
    # Count the number of runs
    num_runs = len(dicts)
    
    # Aggregate the data from each run
    for run_key, run_data in dicts.items():
        recurse(run_data, aggregated_data)

    
    # Calculate the average
    def calculate_average(data, std_dev):
        for k, v in data.items():
            if isinstance(v, dict):
                calculate_average(v,std_dev[k])
            else:
                #v.sort()
                #data[k] = v[RUNS//2]
                data[k] = sum(v) / num_runs
                if len(v) > 1:
                    std_dev[k] = statistics.stdev(v)
                else:
                    std_dev[k] = 0

    std_dev = copy.deepcopy(aggregated_data)
    calculate_average(aggregated_data, std_dev)
    aggregated_data['std_dev'] = std_dev
    return aggregated_data


def parse(exp):
    runs_dict = {}
    with open(observation_dir+exp,'r') as f:
        data = json.load(f)
        #latency
        obs = data['jobs'][0]["read"]
        obs_dict = {}
        obs_dict['latency'] = obs['clat_ns']
        obs_dict['slat'] = obs['slat_ns']
        obs_dict['iops'] = {'min':obs['iops_min'],'max':obs['iops_max'],'mean':obs['iops_mean'],'stddev':obs['iops_stddev'],'N':obs['iops_samples']}
        obs_dict['bw'] = {'min':obs['bw_min'],'max':obs['bw_max'],'mean':obs['bw_mean'],'stddev':obs['bw_dev'],'N':obs['bw_samples']}
        obs_dict['cpu'] = {'usr':data['jobs'][0]["usr_cpu"],'sys':data['jobs'][0]["sys_cpu"],'total':data['jobs'][0]["job_runtime"]}
        if "RUN" in exp:
            try:
                obs_dict['initiator'] = {'reqprocessing':init_reqprocessing(exp)}
                obs_dict['target'] = {'blk':target_blk(exp)}
            except Exception as e:
                pass
                #print("Here", exp, e)

        runs_dict = {}
        runs_dict["latency"] = obs_dict
        
        #throughput
        iops = 0
        bw = 0
        cpu = {}
        flag = False
        for j in range(1,len(data['jobs'])):
            flag = True
            obs = data['jobs'][j]["read"]
            print(data['jobs'][j]["jobname"])
            iops += obs['iops_mean']
            bw += obs['bw_mean']
            #Last cpu
            cpu = {'usr':data['jobs'][j]["usr_cpu"],'sys':data['jobs'][j]["sys_cpu"],'total':data['jobs'][j]["job_runtime"]}
            print(cpu)
        if flag:
            obs_dict = {}
            obs_dict['iops'] = iops
            obs_dict['bw'] = bw 
            obs_dict['iops_across'] = iops/len(data['jobs'])
            obs_dict['cpu'] = cpu
            runs_dict["throughput"] = obs_dict
    return runs_dict



all_observations = {}
#experiments = ["local_same_stonewall.json","local_nice_stonewall.json","local_nice_diff_core.json","local_prio_diff_core.json","remote_nice_prio_same_core.json","local_nice_prio_same_core.json","local_prio_same_core.json","remote_prio_same_core.json","local_diff_core.json","remote_nice_same_core.json","local_nice_same_core.json","local_same_core.json","local_stonewall.json","remote_diff_core.json","remote_same_core.json","remote_stonewall.json"]
experiments = os.listdir(observation_dir)
done = []
for exp in experiments:
    if "crunched" in exp:
        continue
    loopFlag = False
    #if "RUN" in exp:
    loopFlag = True
    if "RUN1" not in exp:
        continue
    
    try:
        #Reduce the RUNS to avg
        if loopFlag:
            runs_dict = {}
            try:
                for i in ["RUN{}".format(j) for j in range(1, RUNS+1)]:
                    runs_dict[i] = parse(exp[:-10]+"_"+i+".json") 
            except:
                pass
            op = reduce(runs_dict)
            for i in op.keys():
                all_observations[exp[:-10]+"_"+i] = op[i]

        else: 
            op = parse(exp)
            for i in op.keys():
                all_observations[exp[:-5]+"_"+i] = op[i]

        print(exp)
    except Exception as e:
        print(exp, e)


#sys.exit(0)
with open(observation_dir+'crunched_numbers_qos.json','w') as f:
    json.dump(all_observations, f)
