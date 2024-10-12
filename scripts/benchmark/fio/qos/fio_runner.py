import os
import time
import sys
import subprocess
#import confirm_tool
import signal
import re

observation_dir="../../../../observations/qos2/"
confidence_level = 0.95
error_bound = 0.05
log_dir = "./logs/"

node = sys.argv[1] #type_fop_bop
number_of_bprocess = [1]
block_size_of_bprocess = ["4k"]

RUNS = 3
LOAD = [10*i for i in range(10)]
LOAD = [20,40,60,80,100]
bop = "randread"
if "bwrite" in node:
    bop = "randwrite"

fop = "randread"
runtime = "120"
warmup = "60"
if "fwrite" in node:
    fop = "randwrite"
    runtime = str(5*60)
    warmup = str(5*60)


if "ID_TD_SS" in node:
    number_of_bprocess=[5]


if "ID_TS_SD" in node:
    number_of_bprocess=[2,3,4,5,6]


if "ICS_TD_SD" in node:
    number_of_bprocess=[1,2,3,4,5]

#QD = [2**i for i in range(9)]
QD = [1, 128]
def list_all_experiments():
    experiments = []
    for load in LOAD:
        for qd in QD:
            for bp in number_of_bprocess:
                for i in range(1, RUNS+1):
                    pmtrs = {}
                    pmtrs["FDEVICE"] = os.environ["FDEVICE"]
                    pmtrs["BDEVICE"] = os.environ["BDEVICE"]
                    pmtrs["RUN"] = str(i)
                    bbs = block_size_of_bprocess[0]
                    pmtrs["BBSIZE"] = bbs
                    pmtrs["BCOUNT"] = str(bp)
                    pmtrs["NAME"] = "{}_SSD_QD{}_LOAD{}_P{}_RUN{}".format(node, qd, load, bp, i)
                    pmtrs["FOP"] = fop
                    pmtrs["BOP"] = bop
                    pmtrs["FQD"] = str(qd)
                    if load != 0:
                        #Limit per process
                        pmtrs["IOPS_LIM"] = str((int(os.environ["MAX_IOPS"])* 1000 * load/100)/bp)
                    experiments.append(pmtrs)
    return experiments

def set_experiment_parameters(parameters):
    for key in parameters.keys():
        os.environ[key] = parameters[key]

def run_fio(fio, op):
    with open(op, 'w') as File:
        subprocess.run("fio --output-format=json {}".format(fio), shell=True, text=True, stdout=File)


def erase_and_pre_condition(device):
    print("Pre conditioning device : ", device)
    subprocess.run("nvme format "+device, shell=True, text=False)
    #Set the device
    os.environ["DEVICE"] = device
    run_fio("pre_condition.fio", "/dev/null")


def statisticaly_valid(exp_name, entries):
    return True
    parameters = ["clat","bw","iops"]
    for para in parameters:
        file_path = "{}{}_{}.log".format(log_dir, exp_name, para)
        obs = confirm_tool.get_obs_from_log(file_path)
        if len(obs) == 0:
            return False
        #Remove the logs during RAMP time
        obs = obs[10:]
        #Reduce observations
        valid = confirm_tool.apply_confirm(obs, confidence_level, error_bound)
        if not valid:
            return False

    return True


#**************Main***********************
experiments = list_all_experiments()
count_experiment = 0
total_experiments = len(experiments)
print("Total number of experiments : ", total_experiments)
for experiment_parameters in experiments:
    count_experiment += 1
    print("***************************************************")
    print("Experiment({}/{}):".format(count_experiment, total_experiments),experiment_parameters["NAME"])
    #Get output file name
    output_file_name = experiment_parameters["NAME"] + ".json"
    op = observation_dir + output_file_name

    #Set the environemnt variables for the experiment
    set_experiment_parameters(experiment_parameters)
    for iter_count in range(1, 16):
        os.environ["RUNTIME"] = runtime
        os.environ["WARMUP"] = warmup

        #Run the fio
        print("{}) Executing experiment".format(iter_count)) 
        
        #Run bpf   
        #subprocess.run(["curl","http://127.0.0.1:8080/bpf?script={}&id={}".format("blk_initiator_processing.bt",experiment_parameters["NAME"]+"_initiator_reqprocesstime")])

        #Start CPU usage 
        #subprocess.run(["curl","http://172.16.137.2:8080/start?id={}".format(experiment_parameters["NAME"]+"_target_cpu")])
        
        #Start the target micro
        #subprocess.run(["curl","http://172.16.137.2:8080/bpf?script={}&id={}".format("target_micros.bt",experiment_parameters["NAME"]+"_target_micro")])

        if experiment_parameters["BCOUNT"] == "0":
            run_fio("lt0.fio", op)
        else:
            run_fio("lt.fio", op)
       
        #Stop the target micro
        #subprocess.run(["curl","http://172.16.137.2:8080/sbpf?script={}&id={}".format("target_micros.bt",experiment_parameters["NAME"]+"_target_micro")])

        #Stop CPU usage
        #subprocess.run(["curl","http://172.16.137.2:8080/stop?id={}".format(experiment_parameters["NAME"]+"_target_cpu")])

        #subprocess.run(["curl","http://127.0.0.1:8080/sbpf?script={}&id={}".format("blk_initiator_processing.bt",experiment_parameters["NAME"]+"_initiator_reqprocesstime")])

        #Parse the output to get latency, IOPS, bandwidth and percentile distribution 
        #Check the statistical validity with confirm tool
        if statisticaly_valid(experiment_parameters, iter_count * 5):
            break
        break
