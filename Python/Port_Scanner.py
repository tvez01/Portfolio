import socket
import sys
from datetime import datetime
import threading
from queue import Queue
import os

# Define the number of threads to use
NUMBER_OF_THREADS = 100
queue = Queue()
open_ports = []

# Function to clear the screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to scan a single port
def port_scan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Set timeout to 1 second
        result = sock.connect_ex((targetIP, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    except:
        pass

# Threader task
def threader():
    while True:
        worker = queue.get()
        port_scan(worker)
        queue.task_done()

# Input target host
target = input("Enter the host to be scanned: ")
targetIP = socket.gethostbyname(target)
print("Starting scan on host: ", targetIP)

# Clear the screen in a cross-platform way
# clear_screen()

# Start timing the scan
t1 = datetime.now()

# Creating threads
for x in range(NUMBER_OF_THREADS):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

# 100 jobs assigned.
for worker in range(1, 1025):
    queue.put(worker)

# Wait until the thread terminates.
queue.join()

# Scanning finished
print("Open ports:", sorted(open_ports))

t2 = datetime.now()
total = t2 - t1
print('Scanning Completed in: ', total)