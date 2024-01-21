# report_abuse.py
import csv
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(current_directory, 'data', 'abuse_reports.csv')

def read_abuse_reports():
    with open(csv_file_path, 'r', newline='') as file:
        reader = csv.DictReader(file)
        return list(reader)

def write_abuse_report(report):
    fieldnames = ['abuse_type', 'description']
    with open(csv_file_path, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(report)

def get_abuse_reports():
    return read_abuse_reports()

def add_abuse_report(report):
    write_abuse_report(report)
