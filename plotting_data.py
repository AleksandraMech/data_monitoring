
import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# aby stworzyć testowy plik csv, na podstawie którego będzie tworzony wykres
import csv
import random
import time

x_value = 0
total_1 = 1000
total_2 = 1000

fieldnames = ["x_value", "total_1", "total_2"]  #headers for csv file


with open('data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

while True:

    with open('data.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        info = {
            "x_value": x_value,
            "total_1": total_1,
            "total_2": total_2
        }

        csv_writer.writerow(info)
        print(x_value, total_1, total_2)

        x_value += 1
        total_1 = total_1 + random.randint(-6, 8)
        total_2 = total_2 + random.randint(-5, 6)

    time.sleep(1)

    x_vals = []
    y_vals = []
    MAX_FRAMES = 100

    index = count()


    def animate(i):
        data = pd.read_csv('data.csv')
        x = data['x_value']
        y1 = data['total_1']
        y2 = data['total_2']

        plt.cla()

        plt.plot(x, y1, label='Channel 1')
        plt.plot(x, y2, label='Channel 2')

        plt.legend(loc='upper left')
        plt.tight_layout()


    ani = FuncAnimation(plt.gcf(), animate, interval=1000, save_count=MAX_FRAMES) #gcf= get current figure ; 1000=1sekunda

    plt.tight_layout()
    plt.show()