import json
import re
import numpy as np
import sys
import os

# Define the input and output file paths
input_path = "../../../monitor/"
files  = os.listdir(input_path)

output_file = "../../../../observations/qos/crunched_micro.json"

# Regular expression pattern to match each microbench line
pattern = r"@microbench\[(\d+)\]: \((\d+), (\d+), (\d+), (\d+), (\d+)\)"

microbench_data = {}

# Open and read the input file
for i in files:
    if 'micro' not in i:
        continue
        
    # Dictionary to hold the parsed data
    pfmicrobench_data = {}
    end_to_end_values = []
    
    with open(input_path+i, "r") as file:
        for line in file:
            # Use regex to find matches
            match = re.match(pattern, line)
            if match:
                key = match.group(1)

                # Create a dictionary for the tuple values
                values = {
                    "block": int(match.group(2)),
                    "nvmeof_initiator": int(match.group(3)),
                    "tcp": int(match.group(4)),
                    "target": int(match.group(5)),
                    "end_to_end": int(match.group(6))
                }

                #sanity check
                if values["block"]+values["nvmeof_initiator"]+values["tcp"]+values["target"] != values["end_to_end"]:
                    continue
                if values["end_to_end"] > 10*(10**9):
                    continue

                # Add the entry to the microbench_data dictionary
                pfmicrobench_data[int(key)] = values

                # Collect the end-to-end value for percentile calculation
                end_to_end_values.append(values["end_to_end"])

    # Calculate the 99th percentile of the 'end_to_end' key
    to_file_data = {}
    print(i,len(end_to_end_values))
    for j in [50, 90, 99]:
        percentile = np.percentile(end_to_end_values, j)
        pkey = min(end_to_end_values, key=lambda x:abs(x-percentile))
        to_file_data[j] = pfmicrobench_data[pkey]

    microbench_data[i] = to_file_data


# Write the parsed data to the JSON output file
with open(output_file, "w") as json_file:
    json.dump(microbench_data, json_file, indent=4)

print(f"JSON output written to {output_file}")

