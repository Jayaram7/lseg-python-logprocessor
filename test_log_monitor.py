# test_log_monitor.py

import unittest
from datetime import timedelta
from log_monitor import parse_log_line, process_logs_from_lines

class TestLogMonitor(unittest.TestCase):

    # Test case for validating the format of the Log
    def test_parse_log_line_valid(self):
        line = "11:40:51,scheduled task 996, START,90962"
        parsed = parse_log_line(line)
        self.assertEqual(parsed['timestamp'].hour, 11)
        self.assertEqual(parsed['description'], "scheduled task 996")
        self.assertEqual(parsed['pid'], "90962")
        self.assertEqual(parsed['action'], "START")

    # Test case for validating the format of the Log
    def test_parse_log_line_invalid(self):
        invalid_line = "Not a valid log line"
        with self.assertRaises(ValueError):
            parse_log_line(invalid_line)

    # Test case for validating the OK Threshold
    def test_process_logs_ok(self):
        logs = [
            "11:38:33,scheduled task 386, START,10515",
            "11:40:24,scheduled task 386, END,10515"
        ]
        result = process_logs_from_lines(logs)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['status'], 'OK')
    
    # Test case for validating the WARN Threshold
    def test_process_logs_warning(self):
        logs = [
            "11:38:33,scheduled task 386, START,10515",
            "11:47:24,scheduled task 386, END,10515"
        ]
        result = process_logs_from_lines(logs)
        self.assertEqual(result[0]['status'], 'WARNING')
        self.assertTrue(result[0]['duration'] >= timedelta(minutes=6))

    # Test case for validating the Error Threshold
    def test_process_logs_error(self):
        logs = [
            "11:38:33,scheduled task 386, START,10515",
            "11:57:24,scheduled task 386, END,10515"
        ]
        result = process_logs_from_lines(logs)
        self.assertEqual(result[0]['status'], 'ERROR')
        self.assertTrue(result[0]['duration'] >= timedelta(minutes=11))

    # Test case for validating the logs for incomplete logs
    def test_incomplete_jobs(self):
        logs = [
            "11:38:33,scheduled task 386, START,10515"
            # Missing END
        ]
        result = process_logs_from_lines(logs)
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()