```markdown
# 🔍 Log Monitoring Application

A Python-based log monitoring tool that parses job log files, calculates processing durations, and flags slow jobs with warnings or errors based on configurable thresholds.

---

## 📌 Features

- ✅ Parses structured logs with timestamp, job description, PID, and status (`START` / `END`)
- ⏱️ Measures duration between job `START` and `END`
- ⚠️ Logs a **warning** if a job takes longer than 5 minutes
- ❌ Logs an **error** if a job takes longer than 10 minutes
- 🧪 Includes unit tests for robustness

---

## 📂 Log File Format

Each log line must follow this format:

HH:MM:SS,Job Description, START|END, PID

## Log File Format Example:

11:38:33,scheduled task 386, START,10515
11:39:26,background job dej, START,90812
11:40:24,scheduled task 386, END,10515

---

## 🚀 Getting Started

### 📋 Requirements

- Python 3.7+
- No external libraries required

### 🔧 Installation

Clone this repository using below commands:

git clone https://github.com/Jayaram7/lseg-python-logprocessor.git
cd lseg-python-logprocessor

Place your log file in the project directory as `logs.log` or modify the script to use a custom filename.

---

## 📈 Usage

Run the main script:

`python log_monitor.py`

---

## 🧪 Running Tests

Unit tests are included in `test_log_monitor.py`.

To run tests:


`python -m unittest test_log_monitor.py`

---

## 📁 File Structure

├── logs.log              # Sample or real log file
├── log_monitor.py        # Main processing script
└── test_log_monitor.py   # Unit tests for the application


---