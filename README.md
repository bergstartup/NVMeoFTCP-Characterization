# NVMeoFTCP-Characterization

This repository contains experiment scripts and artifacts for my MSc thesis on performance of NVMeoF-TCP.

<h1>Experiments</h1>
<h2>RQ1: What are the performance implications of NVMeoF-TCP configurations?</h2>
<h3>Pollable I/O queues in the initiator</h3>
<pre>
cd scripts/benchmark/fio/performance
./poll_npoll.sh #Executes the experiment and fio output are stored in observations/performance/
python3 crunching.py  #Creates a lean .json file with required metrics for all experiment
</pre>
<h3>Target polling</h3>
