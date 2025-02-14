import multiprocessing
import time
import random

def writer(id, write_lock, shared_resource, reader_count, reader_count_lock):
    while True:
        time.sleep(random.randint(1, 5))
        while True:
            with reader_count_lock:
                print(f"Writer-{id} waiting")
                if reader_count.value == 0:
                    break
            time.sleep(0.1)
        
        with write_lock:
            print(f"Writer-{id} started writing")
            shared_resource.value += 1
            time.sleep(1)
        
      

def reader(id, write_lock, shared_resource, reader_count, reader_count_lock):
    while True:
        time.sleep(random.randint(1, 3))
        with reader_count_lock:
            reader_count.value += 1
        
        print(f"Reader-{id} is reading the shared resource: {shared_resource.value}")
        time.sleep(1)
        
        with reader_count_lock:
            reader_count.value -= 1

def process_manager(num_readers, num_writers):
    write_lock = multiprocessing.Lock()
    reader_count_lock = multiprocessing.Lock()
    reader_count = multiprocessing.Value('i', 0)
    shared_resource = multiprocessing.Value('i', 0)
    processes = []

    for i in range(num_readers):
        p = multiprocessing.Process(target=reader, args=(i + 1, write_lock, shared_resource, reader_count, reader_count_lock))
        processes.append(p)
        p.start()

    for i in range(num_writers):
        p = multiprocessing.Process(target=writer, args=(i + 1, write_lock, shared_resource, reader_count, reader_count_lock))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

if __name__ == "__main__":
    num_readers = 3
    num_writers = 1
    process_manager(num_readers, num_writers)
