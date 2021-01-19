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
    purchasingPow = 5;
    eco = [carbonPrice, purchasingPow]
    while True:
        purchasingPow = purchasingPow + random.randint(-1, 1)
        eco = [carbonPrice, purchasingPow]
        qEco.put(eco)


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
    conso = 10"""
    p = Process(target = runMarket, args = (0.16, b,))
    p.start()
    p.join()
