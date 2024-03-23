import threading

import time



class Semaphore:

    def __init__(self, initial):

        self.lock = threading.Lock()

        self.value = initial



    def P(self):

        with self.lock:

            while self.value == 0:

                pass

            self.value -= 1



    def V(self):

        with self.lock:

            self.value += 1



class Mutex:

    def __init__(self):

        self.lock = threading.Lock()



    def acquire(self):

        self.lock.acquire()



    def release(self):

        self.lock.release()



def own_implementation():

    mutex = Mutex()

    wrt = Semaphore(1)

    readCount = Semaphore(1)

    num_reads = 0

    num_writes = 0



    file = open("input.txt", "a+")

    output_file = open("output.txt", "w")



    def writer(thread_num):

        nonlocal num_writes

        for i in range(5):  # Perform 5 writes

            wrt.P()

            file.write(f"Thread {thread_num} writes line {i+1}\n")

            wrt.V()

            num_writes += 1

            if num_writes == 10:

                return



    def reader(thread_num):

        nonlocal num_reads

        for i in range(5):  # Perform 5 reads

            readCount.P()

            if readCount.value == 1:

                wrt.P()

            readCount.V()

            last_line = None

            with open("input.txt", "r") as f:

                last_line = f.readlines()[-1].strip()

            output_file.write(f"Thread {thread_num} reads: {last_line}\n")

            num_reads += 1

            if num_reads == 10:

                return

            if readCount.value == 1:

                wrt.V()



    writer_threads = []

    reader_threads = []



    for i in range(2):

        writer_threads.append(threading.Thread(target=writer, args=(i,)))

        reader_threads.append(threading.Thread(target=reader, args=(i,)))



    for thread in writer_threads + reader_threads:

        thread.start()



    for thread in writer_threads + reader_threads:

        thread.join()



    file.close()

    output_file.close()



def library_implementation():

    mutex = threading.Lock()

    wrt = threading.Semaphore(1)

    readCount = threading.Semaphore(1)

    num_reads = 0

    num_writes = 0



    file = open("input.txt", "a+")

    output_file = open("output.txt", "w")



    def writer(thread_num):

        nonlocal num_writes

        for i in range(5):  # Perform 5 writes

            wrt.acquire()

            file.write(f"Thread {thread_num} writes line {i+1}\n")

            wrt.release()

            num_writes += 1

            if num_writes == 10:

                return



    def reader(thread_num):

        nonlocal num_reads

        for i in range(5):  # Perform 5 reads

            readCount.acquire()

            if readCount._value == 1:

                wrt.acquire()

            readCount.release()

            last_line = None

            with open("input.txt", "r") as f:

                last_line = f.readlines()[-1].strip()

            output_file.write(f"Thread {thread_num} reads: {last_line}\n")

            num_reads += 1

            if num_reads == 10:

                return

            if readCount._value == 1:

                wrt.release()



    writer_threads = []

    reader_threads = []



    for i in range(2):

        writer_threads.append(threading.Thread(target=writer, args=(i,)))

        reader_threads.append(threading.Thread(target=reader, args=(i,)))



    for thread in writer_threads + reader_threads:

        thread.start()



    for thread in writer_threads + reader_threads:

        thread.join()



    file.close()

    output_file.close()



if __name__ == "__main__":

    print("Own Implementation:")

    start_time = time.time()

    own_implementation()

    print("Time taken:", time.time() - start_time)



    print("\nLibrary Implementation:")

    start_time = time.time()

    library_implementation()

    print("Time taken:", time.time() - start_time)

