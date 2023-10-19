import csv
import os

from datetime import datetime

with open('example.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)

    with open('new_example_{str(datetime.now())}.csv', 'w') as new_file:
        csv_writer = csv.writer(new_file, delimiter='\t')  # \t = tab

        for line in csv_reader:
            csv_writer.writerow(line)