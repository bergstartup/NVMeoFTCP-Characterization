# NVMeoFTCP-Characterization

This repository contains experiment setup, scripts and artifacts for my MSc thesis on performance of NVMeoF-TCP.

<h1></h1>

<h1>Setup</h1>
<h2>In target</h2>
<h2>In initiator</h2>

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


<h2>RQ3: What is the performance interference with various loads on compute resources in NVMeoF-TCP?</h2>
<h3>Initiator interference</h3>
<h3>Target interference</h3>
