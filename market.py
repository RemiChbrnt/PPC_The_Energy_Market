""" notes : il faudrait purchasingPow entre -5 et 5
            il faudrait que carbonPrice soit la différence entre le prix du carbone avant et maintenat
            il faudrait définir un prix de base (genre celui de la première itération)
            il faudrait que conso soit aussi une différence (comme ça si elle est négative le prix baisse et inversement)"""

# KWh Price : 0.16 €
import time
import os
import sysv_ipc
import threading

from multiprocessing import Process
from queue import Queue

def runMarket(initPrice, b):
    mqMarket = sysv_ipc.MessageQueue(256)
    day = 0
    isTsunami = False
    isTechnicalFailure = False
    isVirus = False
    isFreeEnergyDay = False

    carbonPrice = 0.001
    politic = False
    purchasingPow = 5
    conso = 10
    price = initPrice
    print("#DEBUG MARKET :: Starting market")
    while True:
        price = price * (1 + conso * 0.001)
        if isFreeEnergyDay == True :
            price = 0
        else :
            price = price + 0.02 * (carbonPrice + purchasingPow/10)
            if politic == True :
                price += 0.03
            if isTechnicalFailure == True :
                price += 0.015
            if isVirus == True :
                price += 0.02
            if isTsunami == True :
                price += 0.025
        print("#DEBUG MARKET :: Day %d : price is %.2f" % (day, price))
        b.wait()
        day +=1




def economics (qEco) :
    carbonPrice = 0.001
    purchasingPow = 5
    eco = [carbonPrice, purchasingPow]
    while True:
        purchasingPow = purchasingPow + random.randint(-1, 1)
        eco = [carbonPrice, purchasingPow]
        qEco.put(eco)



def politics ():
    degPol = 7
    while True :
        degPol = degPol + random.randint(-1, 1)
        pid = os.getppid()
        if degPol <=3 :
            os.kill(pid, signal.SIGUSR1)

def cataclysme ():
    probVirus = random.uniform(0, 1)
    probFailure = random.uniform(0, 1)
    probFree = random.uniform(0, 1)
    probTsunami = random.uniform(0, 1)
    pid = os.getppid()
    if probVirus < 0.07 :
        os.kill(pid, signal.SIGPROF)
    if probFailure < 0.1 :
        os.kill(pid, signal.SIGUSR2)
    if probFree < 0.04 :
        os.kill(pid, signal.SIGIOT)
    if probTsunami < 0.01 :
        os.kill(pid, signal.SIGWINCH)

def signaux (sig,frame):
    global politic
    global isTechnicalFailure
    global isFreeEnergyDay
    global isTsunami
    global isVirus

    if sig == signal.SIGUSR1 :
        lockPol.acquire()
        politic = True
        lockPol.release()
    if sig == signal.SIGUSR2 :
        lockFailure.acquire()
        isTechnicalFailure = True
        lockFailure.release()
    if sig == signal.SIGIOT :
        lockFree.acquire()
        isFreeEnergyDay = True
        lockFree.release()
    if sig == signal.SIGWINCH :
        lockTsunami.acquire()
        isTsunami = True
        lockTsunami.release()
    if sig == signal.SIGPROF :
        lockVirus.acquire()
        isVirus = True
        lockVirus.release()



def run(b):
    """qEco = Queue()
    #lancement process economics
    pEco = Process(target = economics, args = (qEco,))
    pEco.start()
    pEco.join()

    resEco = q.get()
    precedPrice = 0.1
    carbonPrice = res [0]
    purchasingPow = res[1]

    politic = false
    isTechnicalFailure = false
    isVirus = false
    isFreeEnergyDay = false
    isTsunami = false


    #redirection des signaux
    signal.signal(signal.SIGUSR1, signaux) #pour politic
    signal.signal(signal.SIGUSR2, signaux) #pour isTechnicalFailure
    signal.signal(signal.SIGIOT, signaux) #pour isFreeEnergyDay
    signal.signal(signal.SIGWINCH, signaux) #pour isTsunami
    signal.signal(signal.SIGPROF, signaux) #pour isVirus

    lockPol = threading.Lock()
    lockFailure = threading.Lock()
    lockVirus = threading.Lock()
    lockFree = threading.Lock()
    lockTsunami = threading.Lock()

    pCata = Process(target = cataclysme, args =(,))
    pCata.start()
    pCata.join()

    conso = 10 #à mettre en lien avec les homes

    p = Process(target = energPriceChang, args = (precedPrice, carbonPrice, purchasingPow, politic, isTechnicalFailure, isVirus, isFreeEnergyDay, isTsunami, conso,))

    conso = 10"""
    p = Process(target = runMarket, args = (0.16, b,))
    p.start()
    p.join()
