import psutil
import time

def get_cpu_utilization(interval=1):
    """
    Get the CPU utilization percentage.

    :param interval: The interval in seconds to measure the CPU utilization over.
    :return: CPU utilization percentage.
    """
    # Measure CPU utilization over the given interval
    cpu_utilization = psutil.cpu_percent(interval=interval)
    return cpu_utilization

def main():
    # Get the CPU utilization
    cpu_utilization = get_cpu_utilization()
    
    # Print the CPU utilization
    print(f"CPU Utilization: {cpu_utilization}%")

if __name__ == "__main__":
    main()

