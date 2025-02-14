import threading
import time

# Create a semaphore with an initial value of 1
semaphore = threading.Semaphore(1)

def process_p1():
    # P1 acquires the semaphore
    semaphore.acquire()
    print("Process P1 is executing...")
    time.sleep(2)  # Simulate some work
    print("Process P1 has finished execution.")
    # Release the semaphore for P2 to proceed
    #semaphore.release()

def process_p2():
    # P2 tries to acquire the semaphore
    semaphore.acquire()
    print("Process P2 is executing...")
    time.sleep(2)  # Simulate some work
    print("Process P2 has finished execution.")
    # Release the semaphore (not strictly necessary here)
    semaphore.release()

# Create threads for P1 and P2
thread1 = threading.Thread(target=process_p1)
thread2 = threading.Thread(target=process_p2)

# Start P1 first
thread1.start()
thread1.join()

semaphore.release()
thread2.start()
# Wait for P1 to finish before starting P2

# Start P2

# Wait for P2 to finish
thread2.join()

print("Both processes have completed execution.")
