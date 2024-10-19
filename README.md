# NVMeoFTCP-Characterization

This repository contains experiment setup, scripts and artifacts for my MSc thesis on performance of NVMeoF-TCP.

<h1>Initialization</h1>
<h2>In target</h2>
<pre>
#Register NVMe SSDs to the NVMeoF-TCP module
cd scripts/setup
./nvmeof_target_init.sh <device> <count>
#Execute the HTTP server(Blocking) in the target for dynamic modification of target configurations for experiments
cd scripts/monitor
python3 remoteServer.py
</pre>

<h2>In initiator</h2>
No explicit initialization is required in the initiator as each experiment configures depending on the experiment parameters.

<h1>Experiments</h1>
<h2>RQ1: What are the performance implications of NVMeoF-TCP configurations?</h2>
<h3>Pollable I/O queues in the initiator</h3>
<pre>
cd scripts/benchmark/fio/performance
#Execute the experiment
./poll_npoll.sh 
#fio output are stored in observations/performance/
#Creates a lean .json file with required metrics for all experiment
python3 crunching.py 
</pre>

<h3>Target polling</h3>
<pre>
cd scripts/benchmark/fio/performance
#Execute the experiment
./tpoll.sh 
#fio output are stored in observations/performance/
#Creates a lean .json file with required metrics for all experiment
python3 crunching.py  
</pre>


<h2>RQ2: What is the performance overhead of NVMeoF-TCP compared to local NVMe?</h2>
<h3>For local NVMe and NVMeoF-TCP(localhost) performance numbers</h3>
<pre>
  #Run the following in the initiator
  cd scripts/benchmark/fio/performance/
  ./local_bench.sh
  ./local_tcp.sh
</pre>
<h3>For remote NVMeoF-TCP performance numbers</h3>
<pre>
  #Run the following in the target
  cd scripts/benchmark/fio/performance
  ./remote_bench.sh
  #To copy performance numbers of local NVMe and NVMeoF-TCP(localhost) from the initiator
  ./copy_local.sh
  python3 crunching.py
</pre>

<h2>RQ3: What is the performance interference with various loads on compute resources in NVMeoF-TCP?</h2>
<h3>Initiator interference</h3>
<pre>
  #Run the following in the initiator
  cd scripts/benchmark/fio/qos
  ./initiator.sh
  python3 crunching.py
</pre>
<h3>Target interference</h3>
<pre>
  #Run the following in the initiator
  cd scripts/benchmark/fio/qos_ns
  ./target.sh
  python3 crunching.py
</pre>

<h1>Graphs</h1>
To obtain graphs of the above experiments run the following in the initiator
<ol>
  <li>Collect the local numbers from the target if required </li>
  <li>Run crunching.py in performance, qos, qos_ns</li>
  <li>All the graphs shown in the thesis can be reproduced with collected experiment data visualizer.py in ./observations</li>
</ol>
</ol>
