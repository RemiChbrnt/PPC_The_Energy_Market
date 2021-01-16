import random
import time
import concurrent.futures
import os
import threading
import sysv_ipc

key = 128



def home(initCons, initProd, status, name, barrier):
    day = 0
    print("DEBUG HOME :: House %s: starting" % name)
    while True:
        print("DEBUG HOME :: House %s: Day %d | Cons %s | Prod %s)


    if status == True {


    }

    #    print("Fils: os.getpid() = %s, os.getppid() = %s \n" % (os.getpid(), os.getppid()))
    
        time.sleep(2)
        barrier.wait()
        day += 1
    print("Thread %s: finishing" % name)

