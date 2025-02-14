import threading
import time
import random

def writer(id, write_lock, shared_resource):
    while True:
        
        write_lock.acquire()
        try:
            print(f"Writer-{id} started writing")
            shared_resource["value"] += 1
            time.sleep(1)
            print(f"Writer-{id} finished writing. Shared Resource: {shared_resource['value']}")
        finally:
            
            write_lock.release()
        time.sleep(1)

def reader(id, write_lock, shared_resource):
    while True:
        time.sleep(random.randint(1, 3))
        
        if write_lock.acquire(blocking=False):
            try:
                print(f"Reader-{id} is reading the shared resource: {shared_resource['value']}")
                time.sleep(1)
            finally:
                
                write_lock.release()
        else:
            print(f"Reader-{id} is waiting as Writer is accessing the resource.")
            time.sleep(1)

def thread_manager(num_readers, num_writers):
    
    write_lock = threading.Semaphore(1)
    shared_resource = {"value": 0}  
    threads = []

    
    for i in range(num_writers):
        t = threading.Thread(target=writer, args=(i + 1, write_lock, shared_resource))
        threads.append(t)
        t.start()

    
    for i in range(num_readers):
        t = threading.Thread(target=reader, args=(i + 1, write_lock, shared_resource))
        threads.append(t)
        t.start()

    
    for t in threads:
        t.join()

if __name__ == "__main__":
    num_readers = 3
    num_writers = 1
    thread_manager(num_readers, num_writers)
