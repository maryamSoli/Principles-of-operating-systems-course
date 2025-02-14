import threading
import time
import random


class ReaderPriorityReaderWriter:
    def __init__(self):
        self.read_count = 0  
        self.read_count_lock = threading.Semaphore(1)  
        self.resource_access = threading.Semaphore(1)  
        self.shared_resource = {"value": 0}  

    def reader(self, reader_id):
        while True:
            
            self.read_count_lock.acquire()
            self.read_count += 1
            if self.read_count == 1:  # First reader locks the resource
                self.resource_access.acquire()
            self.read_count_lock.release()

            
            print(f"Reader-{reader_id} is reading the shared resource: {self.shared_resource['value']}")
            time.sleep(random.uniform(0.5, 1.5))  

            
            self.read_count_lock.acquire()
            self.read_count -= 1
            if self.read_count == 0:  # Last reader unlocks the resource
                self.resource_access.release()
            self.read_count_lock.release()

            time.sleep(1)  

    def writer(self, writer_id):
        while True:
            #
            print(f"Writer-{writer_id} wants to write.")
            self.resource_access.acquire()  # Ensure exclusive access to the resource
            print(f"Writer-{writer_id} started writing.")
            self.shared_resource["value"] += 1
            time.sleep(random.uniform(1, 2))  
            print(f"Writer-{writer_id} finished writing. Shared Resource: {self.shared_resource['value']}")
            self.resource_access.release()  # Release resource for others

            time.sleep(1)  


def thread_manager(num_readers, num_writers):
    rw = ReaderPriorityReaderWriter()
    threads = []

    
    for i in range(num_readers):
        t = threading.Thread(target=rw.reader, args=(i + 1,))
        threads.append(t)
        t.start()

    
    for i in range(num_writers):
        t = threading.Thread(target=rw.writer, args=(i + 1,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


if __name__ == "__main__":
    num_readers = 3
    num_writers = 1
    thread_manager(num_readers, num_writers)
