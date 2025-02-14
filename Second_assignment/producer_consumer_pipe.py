from multiprocessing import Process, Pipe
import time
import random


buffer_size = 10



def create_items(pipe_1, notify_pipe,data_pipe):
    """Producer process that creates items and adds them to the buffer."""
    output_pipe = pipe_1[1]
    notify_conn = notify_pipe[0]
    dataa_pipe = data_pipe [1]
    pro_counter = 0

    for _ in range(30):
        item = random.randint(0, 1000)

        pro_counter += 1
        dataa_pipe.send(item)
        print(f"Producer: Producing {item}")
        output_pipe.send("produced") 
        

        
        while pro_counter >= buffer_size:  
            print("Producer waiting: Buffer full.")
            time.sleep(1)  
        while notify_conn.poll():
            ack = notify_conn.recv()
            if ack == "consumed":
                pro_counter -= 1

        time.sleep(1)  
    output_pipe.send(None)
    output_pipe.close()


def consume_items(pipe_1, notify_pipe,data_pipe):
    
    input_pipe = pipe_1[0]
    notify_conn = notify_pipe[1]
    dataa_pipe = data_pipe [0]
    con_counter = 0

    while True:
        
        
        ack = input_pipe.recv()
        if ack == "produced":
            con_counter += 1

        con_counter -= 1
        j =dataa_pipe.recv()
        print(f"Consumer: Consumed {j}")
        notify_conn.send("consumed")  

        
        while con_counter == 0:  
            print("Consumer waiting: Buffer empty.")
            time.sleep(0.01)
            break

        while input_pipe.poll():
            ack = input_pipe.recv()
            if ack == "produced":
                con_counter += 1
            elif ack is None:  
                notify_conn.close()
                input_pipe.close()
                return

        time.sleep(0.01)  


if __name__ == "__main__":
   
    pipe_1 = Pipe(True)
    notify_pipe = Pipe(True)
    data_pipe =Pipe(True)
    

    # Create and start producer and consumer processes
    producer = Process(target=create_items, args=(pipe_1, notify_pipe,data_pipe))
    consumer = Process(target=consume_items, args=(pipe_1, notify_pipe,data_pipe))

    producer.start()
    consumer.start()

    # Close unused pipe ends in the main process
    pipe_1[0].close()
    notify_pipe[0].close()

    # Wait for processes to complete
    producer.join()
    consumer.join()

    print("Producer-Consumer processing complete.")
