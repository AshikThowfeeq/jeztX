# tasks.py
from threading import Lock
from time import sleep
from .recognition import final



counter = 0
counter_lock = Lock()


infolder='uploads/From-Local'
ref_folder='uploads/Spider-Man'


def loop(infolder, ref_folder):

    
    global counter
    with counter_lock:
        counter += 1
        print(f"Start Recognition - Run Count: {counter}")
    # Assuming final is another function that you've defined
    final(infolder, ref_folder)
    with counter_lock:
        print(f"Task Completed - Current Count: {counter}")

