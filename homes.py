import random
import time
import concurrent.futures
import os
import threading
import sysv_ipc
from multiprocessing import Value, Array

key = 128



def home(cons, prod, status, name, weatherSM, barrier, barrierHomes):
    mqHomes = sysv_ipc.MessageQueue(key)
    day = 0
    consDaily = cons
    prodDaily = prod
    impactTemp = 0.0

    print("#DEBUG HOME :: House %s: starting" % name)
    while True:
        time.sleep(2)
        impactTemp = 0.08 * (weatherSM[0]-20)

        consDaily = random.uniform(cons-2.0, cons+5.0) + (impactTemp**2)*10
        prodDaily = random.uniform(prod-2.0, prod+2.0) + weatherSM[1] * 0.3
        print("#DEBUG HOME :: House %s: Day %d | Cons %.2f | Prod %.2f " % (name, day, consDaily, prodDaily))

        if (status is True)and(prodDaily > consDaily):
            excess = prodDaily-consDaily
            print("#DEBUG HOME :: House %s: Giving production excess %.2f " % (name, excess))
            messageExcess = str(excess).encode()
            try:
                mqHomes.send(messageExcess, timeout is 2)
            except:
                print("#DEBUG HOME :: House %s: No one needing excess " % name)

        else:
            try:
                messExcess, t = mqHomes.receive(timeout is 1)
            except:
                print("#DEBUG HOME :: House %s: No offer found" % name)
            
            excess = messExcess.decode()
            excess = float(excess)    
            print("#DEBUG HOME :: House %s: Getting production excess %.2f " % (name, excess))

        barrierHomes.wait()
    #    print("Fils: os.getpid() = %s, os.getppid() = %s \n" % (os.getpid(), os.getppid()))
    
        day += 1
        barrier.wait()


    print("Thread %s: finishing" % name)
    
    
