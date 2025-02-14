#Same time
import logging
import threading
import time
import random

LOG_FORMAT = '%(asctime)s %(threadName)-17s %(levelname)-8s %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

# Buffer size
buffer_size = 30
# Shared buffer (list)
buffer = []


# Semaphore for consumer access (initially 0, no items)
consumer_semaphore = threading.Semaphore(0)
# Semaphore for producer access (initially buffer_size, buffer is empty)
producer_semaphore = threading.Semaphore(buffer_size)

items_produced = 0


def consumer():
    global item
    while True:
        # Consumer waits if buffer is empty
        consumer_semaphore.acquire()
        logging.info('Consumer is waiting')

        # Access and process item from the buffer
        if len(buffer) > 0:
            item = buffer.pop(0)
            logging.info('Consumer notify: item number {}'.format(item))
        else:
            logging.info("Consumer is waiting")

        # Release space in the buffer
        producer_semaphore.release()

        # Simulate some processing time
        time.sleep(random.randint(1,3))  # Random sleep between 1-2 seconds

def producer():
    global item, items_produced
    while items_produced < 30: 
        # Producer waits if buffer is full
        producer_semaphore.acquire()
        logging.info('Producer is waiting')  # Changed message for consistency

        # Generate a random item
        item = random.randint(0, 1000)
        logging.info('Producer notify: item number {}'.format(item))

        # Add the item to the buffer (check for space)
        if len(buffer) < buffer_size:
            
            buffer.append(item)
            items_produced += 1 
        else:
            logging.info("Producer is waiting")

        # Release item for consumption
        consumer_semaphore.release()

        # Simulate some production time
        time.sleep(random.randint(1,3))  # Random sleep between 0-3 seconds


def main():
    threads = []
    # Create 5 consumer threads

    
    for _ in range(5):
        thread = threading.Thread(target=consumer)
        thread.start()
        threads.append(thread)

    # Create 1 producer thread
    producer_thread = threading.Thread(target=producer)
    producer_thread.start()
    threads.append(producer_thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    print("Program terminated")


if __name__ == "__main__":
    main()
