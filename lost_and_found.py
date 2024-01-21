# lost_and_found.py
import csv
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
csv_file_path2 = os.path.join(current_directory,'data', 'lost_and_found_animals.csv')

def read_lost_and_found_animals():
    with open(csv_file_path2, 'r', newline='') as file:
        reader = csv.DictReader(file)
        return list(reader)

def write_lost_and_found_animal(animal):
    fieldnames = ['name', 'species', 'description', 'contact']
    with open(csv_file_path2, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(animal)

def get_lost_and_found_animals():
    return read_lost_and_found_animals()

def add_lost_and_found_animal(animal):
    return write_lost_and_found_animal(animal)
