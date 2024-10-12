import os
import time
import sys
import subprocess
import confirm_tool
import signal


observation_dir="../../../../observations/performance_limit/"
confidence_level = 0.95
error_bound = 0.05
log_dir = "./logs/"
NCPUS = 10
node = sys.argv[1] #Either local or remote
devices = {}
#devices["RAM"] = os.environ["S_DEVICE"]
#devices["SSD"] = os.environ["P_DEVICE"]


devices["SSD"] = "/dev/nvme0n1"
workload_type = ["randread"]
queue_depth = [256]
req_size = ["4k"]
number_of_process = [1]
iouring_type = ["iou"]

rate_limit = {}
rate_limit["10"] = "9k" 
rate_limit["20"] = "18k" 
rate_limit["50"] = "50k"
rate_limit["80"] = "80k"
rate_limit["100"] = "97k"

def list_all_experiments():
    experiments = []
    #TODO: Change the order accordingly!
    for rs in req_size:
        for dt in devices.keys():
            for wt in workload_type:
                for qd in queue_depth:
                    for np in number_of_process:
                        for io in iouring_type:
                            for rt in rate_limit.keys():
                                parameters = {}
                                parameters["DEVICE"] = devices[dt]
                                parameters["WORKLOAD"] = wt
                                parameters["QD"] = qd
                                parameters["NPROCESS"] = np
                                parameters["CPUS"] = ','.join(map(str, [i for i in range(np)]))
                                #parameters["CPUS"] = '0'
                                parameters["RLIMIT"] = rate_limit[rt] 
                                parameters["REQSIZE"] = rs
                                parameters["SQPOLL"] = 0
                                parameters["CPOLL"] = 0
                                if 'p' in io:
                                    parameters["CPOLL"] = 1
                                if 's' in io:
                                    parameters["SQPOLL"] = 1
                                parameters["NAME"] = node+"_"+io+"_"+dt+"_"+wt+"_"+"L"+rt
                                experiments.append(parameters)
    return experiments

def set_experiment_parameters(parameters):
    for key in parameters.keys():
        os.environ[key] = str(parameters[key])

def run_fio(fio, op, cpus = [i for i in range(NCPUS)]):
    cpu_string = ','.join(map(str, cpus))
    print(cpu_string)
    with open(op, 'w') as File:
        subprocess.run("taskset -c {} fio --output-format=json {}".format(cpu_string, fio), shell=True, text=True, stdout=File)


def erase_and_pre_condition(device):
    print("Pre conditioning device : ", device)
    subprocess.run("nvme format "+device, shell=True, text=False)
    #Set the device
    os.environ["DEVICE"] = device
    run_fio("pre_condition.fio", "/dev/null")



def statisticaly_valid(exp_name, entries):
    parameters = ["iops"]
    for para in parameters:
        file_path = "{}{}_{}.log".format(log_dir, exp_name, para)
        obs = confirm_tool.get_obs_from_log(file_path)
        
        reduced_obs = []
        if len(obs) == 0:
            print("No observation")
            return False
        elif len(obs) == 1:
            reduced_obs = obs[0]
        else:
            reduced_obs = [sum(values) for values in zip(*obs)]
        
        #Use reduce observations
        valid = confirm_tool.apply_confirm(reduced_obs, confidence_level, error_bound)
        if not valid:
            print("Not converging")
            os.rename(file_path, file_path+"_"+str(entries))
            return False

    return True


def run_yes():
    p = subprocess.Popen(["taskset","-c","0","yes"], stdout=subprocess.DEVNULL)
    return p

def run_tcp_trace(fop):
    p = subprocess.Popen(["bpftrace","../../bpf/tcptrace.bt","-o",fop+"_bpf"])
    time.sleep(5)
    return p

#**************Main***********************
#Execute pre conditioning
for device in devices.keys(): 
    break
    erase_and_pre_condition(devices[device])


print("Running bpf trace to collect keep alive data")
#p = run_tcp_trace(observation_dir + "keep_alive_bpf")
#time.sleep(10)
#p.send_signal(signal.SIGINT)



all_experiments = list_all_experiments()
count_experiment = 0
total_experiments = len(all_experiments)
print("Total number of experiments : ", total_experiments)
for experiment_parameters in all_experiments:
    count_experiment += 1
    print("***************************************************")
    print("Experiment({}/{}):".format(count_experiment, total_experiments),experiment_parameters["NAME"])

    #Get output file name
    output_file_name = experiment_parameters["NAME"]
    op = observation_dir + output_file_name

    #Set the environemnt variables for the experiment
    set_experiment_parameters(experiment_parameters)
    for iter_count in range(2, 16):
        #Set exp time
        os.environ["TIME"] = str(iter_count * 60) 
        print("Running experiment for (sec)",iter_count * 60)
        
        #run tcp_trace
        #p = run_tcp_trace(op)
        #yes = []
        #for i in range(experiment_parameters["BPROCESS"]):
        #    yes.append(run_yes())
        #Run target cpu util
        subprocess.run(["curl","http://172.16.137.2:8080/start?id={}".format(experiment_parameters["NAME"]+"_target_cpu")]) 
        #Run initiator cpu util
        subprocess.run(["curl","http://127.0.0.1:8080/start?id={}".format(experiment_parameters["NAME"]+"_initiator_cpu")])
        #Run the fio
        #run_fio("workload.fio", op, [i for i in range(experiment_parameters["NPROCESS"])])
        run_fio("workload.fio", op)
        #Kill initiator cpu util
        subprocess.run(["curl","http://127.0.0.1:8080/stop?id={}".format(experiment_parameters["NAME"]+"_initiator_cpu")])
        #Kill target cpu util
        subprocess.run(["curl","http://172.16.137.2:8080/stop?id={}".format(experiment_parameters["NAME"]+"_target_cpu")])

        #kill tcp_trace
        #for i in yes:
        #    i.send_signal(signal.SIGINT)
        #p.send_signal(signal.SIGINT)
        break
        #Parse the output to get latency, IOPS, bandwidth and percentile distribution 
        #Check the statistical validity with confirm tool
        if statisticaly_valid(experiment_parameters["NAME"], iter_count):
            break
