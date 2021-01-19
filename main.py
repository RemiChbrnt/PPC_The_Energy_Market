# import weatherBis
import threading
import sysv_ipc
import concurrent.futures
from multiprocessing import Process, Value, Array

import weather
import market
import homes



if __name__ == '__main__':
    weatherSM = Array('f', range(2))
    mqHomes = sysv_ipc.MessageQueue(128, sysv_ipc.IPC_CREAT)
    mqMarket = sysv_ipc.MessageQueue(256, sysv_ipc.IPC_CREAT)
    mqHomes.remove()
    mqMarket.remove()
    mqHomes = sysv_ipc.MessageQueue(128, sysv_ipc.IPC_CREAT)
    mqMarket = sysv_ipc.MessageQueue(256, sysv_ipc.IPC_CREAT)
    
    print("DEBUG MAIN :: Launching Market...")
    pMarket = Process(target=market.runMarket, args=(0.16, 1000, 2000, 40))
    pMarket.start()

    nbHomes = 3 #number of homes to simulate
    b = threading.Barrier(nbHomes+1) #homes and weather synchronize each day

    with concurrent.futures.ThreadPoolExecutor(max_workers=nbHomes+2) as executor:
        print("#DEBUG MAIN :: Simulating Weather...") 
        executor.submit(weather.run, 20.0, weatherSM, b)  #Starting weather in thread pool
        
        print("#DEBUG MAIN :: Creating Homes")
        for i in range(nbHomes): #status :: 0=AlwaysGive 2=AlwaysSell
            if i==0:
                executor.submit(homes.home, 5.0, 0.0, 0, i+1, weatherSM, b)
            else:
                executor.submit(homes.home, 5.0, 3.0, 0, i+1, weatherSM, b)
