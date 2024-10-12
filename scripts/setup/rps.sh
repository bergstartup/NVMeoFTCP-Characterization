#!/bin/bash


#sudo su

echo 32768 > /proc/sys/net/core/rps_sock_flow_entries

# Interface name
IFACE="ens4np0"
# Number of channels/queues
NUM_CHANNELS=$(ls -d /sys/class/net/"$IFACE"/queues/rx-* | wc -l)

# Validate interface existence
if ! ip link show "$IFACE" &> /dev/null; then
    echo "Error: Interface $IFACE does not exist."
    exit 1
fi


ethtool -K $IFACE ntuple on

# Set the RPS flow count for each RX queue
for f in $(seq 0 $((NUM_CHANNELS-1))); do
    RPS_FLOW_CNT_PATH="/sys/class/net/$IFACE/queues/rx-$f/rps_flow_cnt"
    if [ -w "$RPS_FLOW_CNT_PATH" ]; then
        echo 512 | sudo tee "$RPS_FLOW_CNT_PATH" > /dev/null
        echo "Set RPS flow count to 32768 for $RPS_FLOW_CNT_PATH"
    else
        echo "Error: Cannot write to $RPS_FLOW_CNT_PATH"
    fi
done
