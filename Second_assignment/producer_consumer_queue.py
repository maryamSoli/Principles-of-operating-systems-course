from multiprocessing import  Queue
import multiprocessing
import time
import random

buffer_size = 10



class Producer(multiprocessing.Process):
    def __init__(self, queue, data_queue,notify_queue):
        multiprocessing.Process.__init__(self)
        self.queue = queue
        self.data_queue = data_queue
        self.notify_queue = notify_queue

    def run(self):
    
        pro_counter = 0

        for _ in range(30):
            item = random.randint(0, 1000)
            pro_counter += 1
            self.data_queue.put(item)
            print(f"Producer: Producing {item}")
            self.queue.put("produced")

            # Wait if buffer is full
            while pro_counter >= buffer_size:
                print("Producer waiting: Buffer full.")
                time.sleep(0.01)

            # Check for acknowledgments from the consumer
            while not self.notify_queue.empty():
                ack = self.notify_queue.get()
                if ack == "consumed":
                    pro_counter -= 1

            time.sleep(0.01)

        # Signal that production is complete
        self.queue.put(None)


class Consumer(multiprocessing.Process):
    def __init__(self, queue, data_queue,notify_queue):
        multiprocessing.Process.__init__(self)
        self.queue = queue
        self.data_queue = data_queue
        self.notify_queue = notify_queue

    def run(self):
        con_counter = 0

        while True:
            ack = self.queue.get()

            if ack == "produced":
                con_counter += 1

            if con_counter > 0:
                item = self.data_queue.get()
                print(f"Consumer: Consumed {item}")
                self.notify_queue.put("consumed")
                con_counter -= 1

            # Exit when production is complete
            if ack is None:
                print("Consumer: No more items to consume. Exiting.")
                break

            # Wait if buffer is empty
            if con_counter == 0 and self.data_queue.empty():
                print("Consumer waiting: Buffer empty.")
                time.sleep(0.01)
            
            time.sleep(1)


if __name__ == '__main__':
    

    queue= multiprocessing.Queue()
    data_queue = multiprocessing.Queue()
    notify_queue = multiprocessing.Queue()

    # Create the producer and consumer processes
    process_producer = Producer( queue, data_queue,notify_queue)
    process_consumer = Consumer( queue, data_queue,notify_queue)

    # Start the processes
    process_producer.start()
    process_consumer.start()

    # Wait for the processes to finish
    process_producer.join()
    process_consumer.join()
