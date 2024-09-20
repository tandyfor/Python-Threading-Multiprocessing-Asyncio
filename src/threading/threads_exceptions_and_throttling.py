import time
import random
from queue import Queue, Empty
from threading import Thread

import requests
from prettytable import PrettyTable

from secret import TOKEN

THREAD_POOL_SIZE = 4
DATES = ["2020-01-01", "2021-01-01", "2022-01-01", "2023-01-01", "2024-01-01"]

table = PrettyTable()
table.field_names = ["Date", "USD", "GBP", "EUR", "RUB"]

def get_historical_rates(date):
    URL = "https://openexchangerates.org/api/historical/"
    HEADERS = {"Authorization": f"Token {TOKEN}"}
    responce = requests.get(URL + date + ".json", headers=HEADERS)
    if random.randint(0, 5) < 1:
        responce.status_code = 429
    responce.raise_for_status()
    result = responce.json()["rates"]
    return date, result

def present_result(date, result):
    table.add_row([date, result["USD"], result["GBP"], result["EUR"], result["RUB"]])



def worker(work_queue, results_queue):
    while not work_queue.empty():
        try:
            item = work_queue.get(block=False)
        except Empty:
            break
        else:
            try:
                result = get_historical_rates(item)
            except Exception as err:
                results_queue.put(err)
            else:
                results_queue.put(result)
            finally:
                work_queue.task_done()

def main():
    work_queue = Queue()
    results_queue = Queue()

    for date in DATES:
        work_queue.put(date)

    threads = [Thread(target=worker, args=(work_queue, results_queue)) for _ in range(THREAD_POOL_SIZE)]

    for thread in threads:
        thread.start()

    work_queue.join()

    while threads:
        threads.pop().join()

    while not results_queue.empty():
        result = results_queue.get()
        if isinstance(result, Exception):
            raise result
        
        present_result(*result)
    
    print(table)

if __name__ == "__main__":
    s = time.time()
    main()
    e = time.time() - s
    print(f"Time: {e:.2f}s")