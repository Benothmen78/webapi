import csv
import os

# Get the absolute path to the directory of the current script
current_directory = os.path.dirname(os.path.abspath(__file__))
csv_file_path1= os.path.join(current_directory, 'data','adoptable_animals.csv')

def read_adoptable_animals():
    with open(csv_file_path1, 'r', newline='') as file:
        reader = csv.DictReader(file)
        return list(reader)

def write_adoptable_animal(animal):
    fieldnames = ['name', 'species', 'age', 'description', 'contact']
    with open(csv_file_path1, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(animal)

# Add any additional functions related to the adoption process if needed

def get_adoptable_animals():
    return read_adoptable_animals()

def add_adoptable_animal(animal):
    return write_adoptable_animal(animal)
