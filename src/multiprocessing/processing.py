from multiprocessing import Process
import os

def work(identifier):
    print(f"PRC {identifier}; PID: {os.getpid()}")

def main():
    processes = [
        Process(target=work, args=(number, ))
        for number in range(5)
    ]
    for process in processes:
        process.start()
    while processes:
        processes.pop().join()

if __name__ == "__main__":
    main()
