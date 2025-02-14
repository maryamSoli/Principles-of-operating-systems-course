import threading
import time

# Create two semaphores
sem1 = threading.Semaphore(1)
sem2 = threading.Semaphore(1)

class DeadlockTest1(threading.Thread):
    def run(self):
        sem1.acquire()
        print("Thread 1: Acquiring Semaphore 1")
        time.sleep(1)  # Simulating some work
        sem2.acquire()  # This may cause a deadlock
        print("Thread 1: Acquiring Semaphore 2")

class DeadlockTest2(threading.Thread):
    def run(self):
        
        sem2.acquire()
        print("Thread 2: Acquiring Semaphore 2")
        time.sleep(1)  # Simulating some work
        
        sem1.acquire()  # This may cause a deadlock  
        print("Thread 2: Acquiring Semaphore 1")
        

# Create thread instances
tester1 = DeadlockTest1()
tester2 = DeadlockTest2()

# Start the threads
tester1.start()
tester2.start()

# Wait for threads to finish
tester1.join()
tester2.join()

print("Threads finished execution.")
