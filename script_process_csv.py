import csv
import os

from collections import defaultdict
from datetime import datetime
from decimal import Decimal

def process_csv(filename):
    lines = defaultdict(Decimal)

    with open(filename, 'r') as f:
        reader = csv.DictReader(f)


    output_file = f'lines_{str(datetime.now())}.csv'
    with open(os.path.join('output', output_file), 'w') as f:
        writer = csv.writer(f)

        for line in lines.items():
            writer.writerow(line)

    return output_file