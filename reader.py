import serial
import serial.tools.list_ports
from queue import Queue
import csv


class EkgReader:
    def __init__(self, ekg_app, baudrate=96000):
        self.baudrate = baudrate
        self.port = self.find_port()
        self.serial = serial.Serial(self.port, baudrate)
        
        self.data_queue = Queue()  
        self.sample_counter = 0

    
    def read(self):
        if self.port is None:
            print("Brak dostępnego portu szeregowego. Nie można rozpocząć odczytu. \n")
            return
        
        while True:
            data = self.serial.readline()
            data = data.decode().strip()
            self.data_queue.put(data)

            
    def save_to_csv(self, filename):
        if self.port is None:
            print("Brak dostępnego portu szeregowego. Nie można rozpocząć zapisu.")
            return
        
        fieldnames = ['sample','data']
        
        with open(filename, 'w') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()
        
        while True:
            with open(filename, 'a') as csv_file:

                csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                
                data = self.data_queue.get() 
                self.sample_counter += 1

                csv_writer.writerow({'sample': self.sample_counter, 'data': data})
                
                

    def find_port(self):
        ports = list(serial.tools.list_ports.comports())
        if len(ports) == 0:
            print("Nie znaleziono żadnego portu szeregowego.")
            return None
        elif len(ports) > 1:
            print("Wykryto więcej niż jeden port szeregowy. Wybierz numer portu:")
            for i, port in enumerate(ports):
                print(f"{i+1}: {port}")
            selection = input("> ")
            try:
                selection = int(selection)
                if selection < 1 or selection > len(ports):
                    raise ValueError
                port = str(ports[selection-1].device)
            except:
                print("Nieprawidłowy wybór. Używam pierwszego portu.")
                port = str(ports[0].device)
        else:
            port = str(ports[0].device)
        print(f"Wybrano port szeregowy {port}.")
        return port