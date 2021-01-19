import random
import time
import concurrent.futures
import os
import threading
import sysv_ipc
from multiprocessing import Value, Array

def home(cons, prod, status, name, weatherSM, barrier):
    mqHomes = sysv_ipc.MessageQueue(128)
    mqMarket = sysv_ipc.MessageQueue(256)

    day = 0
    consDaily = cons
    prodDaily = prod
    impactTemp = 0.0

    print("#DEBUG HOME :: House %s: starting" % name)
    while True:
        time.sleep(10)
        impactTemp = 0.08 * (weatherSM[0]-20)

        consDaily = random.uniform(cons-2.0, cons+5.0) + (impactTemp**2)*10
        prodDaily = random.uniform(prod-2.0, prod+2.0) + weatherSM[1] * 0.3
        print("#DEBUG HOME :: House %s: Day %d | Cons %.2f kWh | Prod %.2f kWh" % (name, day, consDaily, prodDaily))

        if prodDaily > consDaily:
            excess = prodDaily-consDaily
            if status is 0:
                print("#DEBUG HOME :: House %s: Giving production excess %.2f kWh" % (name, excess))
                messExcess = str(excess).encode()
                mqHomes.send(messExcess)
            else:
                messExcess = (str(excess)+"#SELL").encode()
                mqMarket.send(messExcess)
        else:
            time.sleep(2)
            try:
                messDonation, t = mqHomes.receive(block = False)
                donation = float(messDonation.decode())
                print("#DEBUG HOME :: House %s: Getting production excess %.2f kWh" % (name, donation))
                consDaily -= donation
            except:
                print("#DEBUG HOME :: House %s: No offer found" % name)

            need = consDaily - prodDaily
            if need > 0.0: 
                print("#DEBUG HOME :: House %s: Buying from market %.2f kWh" %(name, need))
                messBuy = (str(need)+"#BUY").encode()
                mqMarket.send(messBuy)
        
        time.sleep(1)
        day += 1
        barrier.wait()
        if name == 1:
            messSynchMarket = ("Homes_DONE").encode()
            mqMarket.send(messSynchMarket)


    print("Thread %s: finishing" % name)
    
    
