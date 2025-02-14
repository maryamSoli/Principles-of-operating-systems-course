# Principles-of-operating-systems-course
This Repository contains the practical assignments that I was working on during this course.
## First assignment
1. Producer-Consumer Problem with Threads
Write a program that implements the producer-consumer algorithm using threads. The program should meet the following conditions:
 * One producer
 * Five consumers
 * Buffer size of 30
   The program should handle various scenarios based on sleep times:
 * Empty buffer: Consumer thread waits for production.
 * Full buffer: Producer thread waits for consumption.
 * Both production and consumption are occurring.
   Each of these scenarios is a separate part of the problem and will be solved by choosing appropriate sleep times and writing separate code for each.
2. Multiple Producers
Repeat the previous problem, but with multiple producers (e.g., 3 producers).
3. Deadlock with Semaphores
Create a deadlock using semaphores.
4. Process Ordering with Semaphores
For two processes, P1 and P2, use semaphores to ensure that P1 always executes before P2, under all conditions.

## Second assignment
1. Write a program that solves the Producer-Consumer problem under the condition that processes must be used instead of threads. There is no shared environment; the necessary information will be stored on both sides. However, data transfer between the producer and consumer will be done using queues and pipes (as two different cases).

Both the producer and the consumer must notify each other whenever an item is produced or consumed.

The solution must cover all three cases: stopping production, stopping consumption, and synchronized production-consumption—making a total of six scenarios.

2. The Readers-Writers problem can also be implemented using processes and locks. However, instead of threads, processes must be used.

Reader and writer priorities must be considered.
