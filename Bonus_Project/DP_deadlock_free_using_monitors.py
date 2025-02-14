# DP deadlock free using monitors
import threading
import time
import random

class DiningPhilosophers:
    THINKING = 0
    HUNGRY = 1
    EATING = 2

    def __init__(self):
        self.state = [self.THINKING] * 5
        self.self = [threading.Condition() for _ in range(5)]
        self.lock = threading.Lock()

    def pickup(self, i):
        with self.lock:
            self.state[i] = self.HUNGRY
            self.test(i)
            if self.state[i] != self.EATING:
                with self.self[i]:
                    self.self[i].wait()

    def putdown(self, i):
        with self.lock:
            self.state[i] = self.THINKING
            self.test((i + 4) % 5)
            self.test((i + 1) % 5)

    def test(self, i):
        if (self.state[(i + 4) % 5] != self.EATING and
            self.state[i] == self.HUNGRY and
            self.state[(i + 1) % 5] != self.EATING):
            self.state[i] = self.EATING
            with self.self[i]:
                self.self[i].notify()

    def initialization_code(self):
        for i in range(5):
            self.state[i] = self.THINKING

def philosopher_thread(philosopher_id, dining_philosophers):
    """
    Simulates the actions of a philosopher.
    """
    while True:
        
        print(f"Philosopher {philosopher_id} is thinking.")
        time.sleep(random.uniform(1, 3))  # Simulate thinking time

        
        print(f"Philosopher {philosopher_id} is hungry.")
        dining_philosophers.pickup(philosopher_id)

        
        print(f"Philosopher {philosopher_id} is eating.")
        time.sleep(random.uniform(1, 2))  # Simulate eating time

       
        print(f"Philosopher {philosopher_id} is done eating.")
        dining_philosophers.putdown(philosopher_id)

def main():
    """
    Sets up and runs the Dining Philosophers simulation.
    """
    num_philosophers = 5
    dining_philosophers = DiningPhilosophers()
    threads = []

    
    for i in range(num_philosophers):
        t = threading.Thread(target=philosopher_thread, args=(i, dining_philosophers))
        threads.append(t)
        t.start()

    
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
