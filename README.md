
# NVMeoFTCP-Characterization

This repository contains the setup, scripts, and artifacts used for my MSc thesis on the performance characterization of NVMe over Fabrics (NVMeoF) using TCP.

## Software Dependencies

The following software are needed to run the benchmarks and to make the plots:
- Fio-3.37
- bpftrace-0.20.2
- Python 3

## Software and Hardware Configuration
All benchmarks run on top of Qemu 6.1.0 with KVM enabled.

**Hardware configuration host (Initiator and Target)**
- 20-core 2.40GHz Intel(R) Xeon(R) Silver 4210R CPU with two sockets connected in NUMA mode. Each socket has ten physical cores and one thread for each core.
- 252GB of DDR4 RAM

**Hardware configuration VM (Initiator)**
- 10-core 2.40GHz Intel(R) Xeon(R) Silver 4210R
- 24GB of DDR4 RAM
- Passthrough of Mellanox ConnectX-5 NIC

**Hardware configuration VM (Target)**
- 10-core 2.40GHz Intel(R) Xeon(R) Silver 4210R
- 24GB of DDR4 RAM
- Passthrough of Mellanox ConnectX-5 NIC
- Passthrough of 2X Western Digital SN540 SSD

The initiator and the target should have a 100Gbps link connected through the Mellanox NIC. The QEMU VM process, memory, and all peripherals should be pinned to the same NUMA domain in the host, both the initiator and target. The Operating System used in the VM is Ubuntu 24.04 with Linux Kernel 6.8.0.

## Initialization

### In Target
To set up the NVMeoF-TCP target:

1. **Register NVMe SSDs to the NVMeoF-TCP module:**
   ```bash
   cd scripts/setup
   ./nvmeof_target_init.sh <device> <count>
   ```
2. **Start the HTTP server (blocking) for dynamic target configuration during experiments:**
   ```bash
   cd scripts/monitor
   python3 remoteServer.py
   ```

### In Initiator
No explicit initialization is required on the initiator side. Each experiment configures the system based on the specific parameters of the test.

## Experiments

### RQ1: What are the performance implications of NVMeoF-TCP configurations?

#### Pollable I/O Queues in the Initiator
To execute experiments related to pollable I/O queues:
```bash
cd scripts/benchmark/fio/performance
./polling_queues.sh <target_ip> <initiator_network_interface>
```

#### Target Polling
To evaluate target-side polling:
```bash
cd scripts/benchmark/fio/performance
./target_polling.sh <target_ip> <initiator_network_interface>
```

### RQ2: What is the performance overhead of NVMeoF-TCP compared to local NVMe?

#### Local NVMe and NVMeoF-TCP (localhost) Performance
Run the following commands on the initiator:
```bash
cd scripts/benchmark/fio/performance/
./local_bench.sh
```

#### Remote NVMeoF-TCP Performance
Run the following commands on the target:
```bash
cd scripts/benchmark/fio/performance
./remote_bench.sh <target_ip> <initiator_network_interface>
```

### RQ3: What is the performance interference with various loads on compute resources in NVMeoF-TCP?

#### Initiator Interference
Execute the following on the initiator:
```bash
cd scripts/benchmark/fio/qos
./initiator.sh <target_ip> <initiator_network_interface>
```

#### Target Interference
Run these commands on the initiator to evaluate target-side interference:
```bash
cd scripts/benchmark/fio/qos_ns
./target.sh <target_ip> <initiator_network_interface>
```

## Generating Graphs

To generate graphs from the experiment results:

1. **Collect local performance data from the target present in observations directory (if needed).**
2. **Run `crunching.py` in each of the following directories:**
   - `performance`
   - `qos`
   - `qos_ns`
3. **Reproduce all thesis graphs using the experiment data:**
   Use visualizer.ipynb in observations directory for reproducing the graphs
