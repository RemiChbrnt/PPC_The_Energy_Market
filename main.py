# import weatherBis
import threading
import concurrent.futures

import homes

if __name__ == '__main__':
    nbHomes = 3
    b = threading.Barrier(3)

    with concurrent.futures.ThreadPoolExecutor(max_workers=nbHomes) as executor:
        print("#DEBUG MAIN :: Creating Homes")
        for i in range(nbHomes):
            executor.submit(homes.home, 5.0, 5.0, 0, i+1, b)

