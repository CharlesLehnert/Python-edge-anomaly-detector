"""
Edge Monitoring System for Naval Equipment
Author: Charles Lehnert
Description: Simulates sensor data (temperature, voltage, vibration), performs anomaly detection,
and logs operational health for edge computing environments. Designed to run locally on edge hardware.
"""

import random
import time
import json
from statistics import mean, stdev

# Configuration for simulated sensors
SENSOR_CONFIG = {
    "temperature": {"min": 19.0, "max": 24.0},
    "vibration": {"min": 0.1, "max": 1.0},
    "voltage": {"min": 110.0, "max": 125.0}
}

# Number of readings and delay
READINGS = 10
DELAY_SEC = 1.0


def generate_sensor_data():
    """Simulates a single batch of sensor readings."""
    return {
        "temperature": round(random.uniform(18.5, 24.5), 2),
        "vibration": round(random.uniform(0.05, 1.1), 2),
        "voltage": round(random.uniform(108.0, 127.0), 2)
    }


def detect_anomalies(data):
    """Detects if any readings are outside of normal thresholds."""
    anomalies = {}
    for sensor, reading in data.items():
        limits = SENSOR_CONFIG[sensor]
        if reading < limits["min"] or reading > limits["max"]:
            anomalies[sensor] = reading
    return anomalies


def health_status(log):
    """Computes average values and gives basic health status."""
    status = {}
    for sensor in SENSOR_CONFIG:
        values = [entry[sensor] for entry in log]
        avg = round(mean(values), 2)
        sd = round(stdev(values), 2) if len(values) > 1 else 0.0
        status[sensor] = {"avg": avg, "std_dev": sd}
    return status


def main():
    print("\n🚢 Starting Edge Monitoring System...\n")
    log = []
    
    for i in range(READINGS):
        data = generate_sensor_data()
        log.append(data)
        anomalies = detect_anomalies(data)

        print(f"Reading {i + 1}: {data}")
        if anomalies:
            print("⚠️  Anomaly Detected:", anomalies)

        time.sleep(DELAY_SEC)

    print("\n🧠 Final Health Summary:")
    summary = health_status(log)
    print(json.dumps(summary, indent=2))

    with open("edge_health_log.json", "w") as f:
        json.dump({"readings": log, "summary": summary}, f, indent=2)
        print("\n📄 Data logged to 'edge_health_log.json'")


if __name__ == "__main__":
    main()
