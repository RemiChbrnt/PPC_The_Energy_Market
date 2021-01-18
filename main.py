# import weatherBis
import threading
import sysv_ipc
import concurrent.futures
from multiprocessing import Process, Value, Array

import weatherBis
import market
import homes

if __name__ == '__main__':
    b = threading.Barrier(4)
    weatherSM = Array('f', range(2)) 
    mqHomes = sysv_ipc.MessageQueue(128, sysv_ipc.IPC_CREAT)
    mqMarket = sysv_ipc.MessageQueue(256, sysv_ipc.IPC_CREAT)
  


    
    nbHomes = 3
    bHomes = threading.Barrier(nbHomes)
    with concurrent.futures.ThreadPoolExecutor(max_workers=nbHomes+1) as executor:
        
        print("#DEBUG MAIN :: Simulating Weather...") 
        executor.submit(weatherBis.run, 20.0, weatherSM, b)
        
        print("#DEBUG MAIN :: Creating Homes")
        for i in range(nbHomes):
            if i==0:
                executor.submit(homes.home, 5.0, 10.0, True, i+1, weatherSM, b, bHomes)
            else:
                executor.submit(homes.home, 5.0, 3.0, True, i+1, weatherSM, b, bHomes)
