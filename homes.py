import random
import concurrent.futures
import signal


def homes(initCons, initProd, status):




if __name__ == "__main__":
    indexes = [random.randint(0, 100) for i in range(10)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        print("Results returned via asynchronous map:")
        for result in executor.map(fibonacci, indexes):
            print(result)

        print("Results returned as Future objects as they complete:")
        futures = [executor.submit(fibonacci, index) for index in indexes]
        for future in concurrent.futures.as_completed(futures):
            print(future.result())