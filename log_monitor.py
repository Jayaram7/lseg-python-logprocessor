# log_monitor.py

import re
from datetime import datetime, timedelta

WARNING_THRESHOLD = timedelta(minutes=5)
ERROR_THRESHOLD = timedelta(minutes=10)

# Log Pattern with regex 
LOG_PATTERN = re.compile(r"(?P<timestamp>\d{2}:\d{2}:\d{2}),(?P<description>.+?), (?P<action>START|END),(?P<pid>\w*\d*)")
   
# This Function helps to match the pattern and initalize the variables with time , description , Process ID i.e pid and action like START/END.   
def parse_log_line(line):
    match = LOG_PATTERN.match(line.strip())  # This line helps us to match the format
    if not match:
        raise ValueError(f"Invalid log format: {line}")
    return {
        "timestamp": datetime.strptime(match.group("timestamp"), "%H:%M:%S"),
        "description": match.group("description").strip(),
        "pid": match.group("pid"),
        "action": match.group("action")
    }

# This function is to process the logs and identify the time interval. Based on the latency , status of the PID will be set to OK , WARNING OR ERROR 
def process_logs_from_lines(log_lines):
    jobs = {}
    results = []

    for line in log_lines:
        log = parse_log_line(line)
        pid = log["pid"]
        if pid not in jobs:
            jobs[pid] = {}
        jobs[pid][log["action"]] = log

    for pid, actions in jobs.items():
        if "START" not in actions or "END" not in actions:
            continue

        start_time = actions["START"]["timestamp"]
        end_time = actions["END"]["timestamp"]
        duration = end_time - start_time
        description = actions["START"]["description"]

        if duration >= ERROR_THRESHOLD:
            status = "ERROR"
        elif duration >= WARNING_THRESHOLD:
            status = "WARNING"
        else:
            status = "OK"

        results.append({
            "pid": pid,
            "description": description,
            "duration": duration,
            "status": status,
            "start": start_time.strftime("%H:%M:%S"),
            "end": end_time.strftime("%H:%M:%S")
        })

    return results

# Display of process in decorative way
def print_report(results):
    for job in results:
        print(f"[{job['status']}] PID {job['pid']} ({job['description']}) - Duration: {job['duration']} (Start: {job['start']}, End: {job['end']})")

def process_logs(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
    return process_logs_from_lines(lines)

if __name__ == "__main__":
    report = process_logs("logs.log")
    print_report(report)
