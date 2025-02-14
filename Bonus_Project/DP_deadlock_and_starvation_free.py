#DP deadlock and starvation free

import threading
from threading import Semaphore
import time
import random

n = 5  # Number of philosophers
philosophers = []
forks = [Semaphore(1) for _ in range(n)]  # Semaphores for forks


def even_philosopher(philosopher_id):
    """
    Function for even-indexed philosophers.
    """
    print(f"Philosopher {philosopher_id} is waiting for forks.")
    forks[philosopher_id].acquire()
    forks[(philosopher_id + 1) % n].acquire()

    # Eating
    print(f"Philosopher {philosopher_id} is eating.")
    time.sleep(random.uniform(1, 2))  # Simulate eating time

    forks[(philosopher_id + 1) % n].release()
    forks[philosopher_id].release()
    print(f"Philosopher {philosopher_id} has finished eating and put down forks.")


def odd_philosopher(philosopher_id):
    """
    Function for odd-indexed philosophers.
    """
    print(f"Philosopher {philosopher_id} is waiting for forks.")
    forks[(philosopher_id + 1) % n].acquire()
    forks[philosopher_id].acquire()

    # Eating
    print(f"Philosopher {philosopher_id} is eating.")
    time.sleep(random.uniform(1, 2))  # Simulate eating time

    forks[philosopher_id].release()
    forks[(philosopher_id + 1) % n].release()
    print(f"Philosopher {philosopher_id} has finished eating and put down forks.")


def main():
    """
    Main function to initialize and run the philosopher threads.
    """
    for i in range(n):
        if i % 2 == 0:
            t = threading.Thread(target=even_philosopher, args=(i,))
        else:
            t = threading.Thread(target=odd_philosopher, args=(i,))
        philosophers.append(t)
        t.start()

    for t in philosophers:
        t.join()


if __name__ == "__main__":
    main()
