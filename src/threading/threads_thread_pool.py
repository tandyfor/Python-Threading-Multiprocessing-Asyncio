import time
from queue import Queue, Empty
from threading import Thread

import requests

from synchronous import get_historical_rates

THREAD_POOL_SIZE = 4
DATES = ["2020-01-01", "2021-01-01", "2022-01-01", "2023-01-01", "2024-01-01"]

def worker(work_queue):
    while not work_queue.empty():
        try:
            item = work_queue.get(block=False)
        except Empty:
            break
        else:
            get_historical_rates(item)
            work_queue.task_done()

def main():
    work_queue = Queue()

    for date in DATES:
        work_queue.put(date)

    threads = [Thread(target=worker, args=[work_queue]) for _ in range(THREAD_POOL_SIZE)]

    for thread in threads:
        thread.start()

    work_queue.join()

    while threads:
        threads.pop().join()

if __name__ == "__main__":
    s = time.time()
    main()
    e = time.time() - s
    print(f"Time: {e:.2f}s")