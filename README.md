
# NVMeoFTCP-Characterization

This repository contains the setup, scripts, and artifacts used for my MSc thesis on the performance characterization of NVMe over Fabrics (NVMeoF) using TCP.

## Initialization

### In Target
To set up the NVMeoF-TCP target:

1. **Register NVMe SSDs to the NVMeoF-TCP module:**
   ```bash
   cd scripts/setup
   ./nvmeof_target_init.sh <device> <count>
   ```
2. **Start the HTTP server (blocking) for dynamic target configuration during experiments:**
   \`\`\`bash
   cd scripts/monitor
   python3 remoteServer.py
   \`\`\`

### In Initiator
No explicit initialization is required on the initiator side. Each experiment configures the system based on the specific parameters of the test.

## Experiments

### RQ1: What are the performance implications of NVMeoF-TCP configurations?

#### Pollable I/O Queues in the Initiator
To execute experiments related to pollable I/O queues:
\`\`\`bash
cd scripts/benchmark/fio/performance
./poll_npoll.sh
# Output is stored in observations/performance/
# Generate a lean .json file with required metrics:
python3 crunching.py
\`\`\`

#### Target Polling
To evaluate target-side polling:
\`\`\`bash
cd scripts/benchmark/fio/performance
./tpoll.sh
# Output is stored in observations/performance/
# Generate a lean .json file with required metrics:
python3 crunching.py
\`\`\`

### RQ2: What is the performance overhead of NVMeoF-TCP compared to local NVMe?

#### Local NVMe and NVMeoF-TCP (localhost) Performance
Run the following commands on the initiator:
\`\`\`bash
cd scripts/benchmark/fio/performance/
./local_bench.sh
./local_tcp.sh
\`\`\`

#### Remote NVMeoF-TCP Performance
Run the following commands on the target:
\`\`\`bash
cd scripts/benchmark/fio/performance
./remote_bench.sh
# To copy performance numbers from the initiator:
./copy_local.sh
python3 crunching.py
\`\`\`

### RQ3: What is the performance interference with various loads on compute resources in NVMeoF-TCP?

#### Initiator Interference
Execute the following on the initiator:
\`\`\`bash
cd scripts/benchmark/fio/qos
./initiator.sh
python3 crunching.py
\`\`\`

#### Target Interference
Run these commands on the initiator to evaluate target-side interference:
\`\`\`bash
cd scripts/benchmark/fio/qos_ns
./target.sh
python3 crunching.py
\`\`\`

## Generating Graphs

To generate graphs from the experiment results:

1. **Collect local performance data from the target (if needed).**
2. **Run `crunching.py` in each of the following directories:**
   - `performance`
   - `qos`
   - `qos_ns`
3. **Reproduce all thesis graphs using the experiment data:**
   \`\`\`bash
   python3 visualizer.py
   \`\`\`
   Ensure the `visualizer.py` script is run from the `./observations` directory.
