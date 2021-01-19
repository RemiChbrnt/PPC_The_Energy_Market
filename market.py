import time
import os
import sysv_ipc
import threading 
import signal
import random

from multiprocessing import Process, Array
from queue import Queue

lockPol = threading.Lock()
lockFailure = threading.Lock()
lockVirus = threading.Lock()
lockFree = threading.Lock()
lockTsunami = threading.Lock()
lockEco = threading.Lock()

    
def sigHandler (sig,frame):
    
    global politic, isTechnicalFailure, isFreeEnergyDay, isTsunami, isVirus 

    if sig == signal.SIGUSR1 :
        lockPol.acquire()
        politic = not politic
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

def runMarket(initPrice, initBal, initEnergy, dailyProd):

    politic = False
    isTechnicalFailure = False 
    isFreeEnergyDay = False
    isTsunami = False
    isVirus = False

    print("#DEBUG MARKET :: Starting market") 
    
    balance = initBal #in €
    storedEnergy = initEnergy #in stored kWh
    price = initPrice #in €
    ecoSM = Array('f', range(2))

    #Redirecting signals
    signal.signal(signal.SIGUSR1, sigHandler) #pour politic
    signal.signal(signal.SIGUSR2, sigHandler) #pour isTechnicalFailure
    signal.signal(signal.SIGIOT, sigHandler) #pour isFreeEnergyDay
    signal.signal(signal.SIGWINCH, sigHandler) #pour isTsunami
    signal.signal(signal.SIGPROF, sigHandler) #pour isVirus
    print("#DEBUG MARKET :: Starting son-processes Economics, Politics and Cataclysm...")


    #launching economics process
    pEco = Process(target = economics, args = (ecoSM,))
    pEco.start()

    #launching cataclysm process
    pCata = Process(target = cataclysm, args =())
    pCata.start()

    #launching cataclysm process
    pPoli = Process(target = politics, args =())
    pPoli.start()

    mqMarket = sysv_ipc.MessageQueue(256) 
    day = 0 
    purchasingPow = 5
    consPreviousDay = 20

    while True:
        with lockEco:
            carbonPrice = ecoSM[0]
            purchasingPow = ecoSM[1]

        price = price*(1 + (consPreviousDay-10)*0.001)
        consPreviousDay = 0
        buyingPrice = price*0.6
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
        isTsunami = False
        isTechnicalFailure = False
        isVirus = False
        isFreeEnergyDay = False
        print("#DEBUG MARKET :: Day %d : price is %.2f €/kWh, Energy Stock is %.2f kWh, Balance is %.2f €" % (day, price, storedEnergy, balance))

        messReceived = ""
        while messReceived != "Homes_DONE":
            try:
                messReceived, t = mqMarket.receive(block = False)    
                messReceived = messReceived.decode()
                instr = messReceived.split("#")
                if len(instr) > 1:
                    amount = float(instr[0])
                    if instr[1] == "BUY":
                        consPreviousDay += amount
                        storedEnergy -= amount
                        amountPrice = amount*price
                        balance += amountPrice    
                        print("#DEBUG MARKET :: Selling %.2f kWh for %.2f" % (amount, amountPrice))
                    elif instr[1] == "SELL":
                        storedEnergy += amount
                        amountPrice = amount*buyingPrice
                        balance -= amountPrice
                        print("#DEBUG MARKET :: Buying %.2f kWh for %.2f" % (amount, amountPrice))
                    else:
                        print("#DEBUG MARKET :: Message Received has unexpected arguments, ignoring request")
            except:
                time.sleep(0.01)
        
        storedEnergy += dailyProd
        balance -= carbonPrice

        #reset variables
        day +=1


            
def economics (ecoSM) :
    print("#DEBUG MARKET :: Starting Economics")
    carbonPrice = 0.001
    purchasingPow = 5
    while True:
        purchasingPow += random.randint(-1, 1)
        carbonPrice += random.uniform(-0.0005, 0.0005)
        with lockEco:
            ecoSM[0] = purchasingPow
            ecoSM[1] = carbonPrice
        time.sleep(5)



def politics ():
    print("#DEBUG MARKET :: Starting Politics")
    degPol = 7
    isWar = False
    while True :
        degPol = degPol + random.randint(-1, 1)
        pid = os.getppid()
        if degPol <=3:
            if isWar == False:
                print("#DEBUG POLITICS :: A War has struck")
                dePol = 2
                isWar = True
                os.kill(pid, signal.SIGUSR1)
        elif isWar == True:
            isWar = False
            degPol = 7
            os.kill(pid, signal.SIGUSR1)
            print("#DEBUG POLITICS :: The war is over")
        time.sleep(5)

def cataclysm ():
    print("#DEBUG MARKET :: Starting Cataclysm")
    while True:
        probVirus = random.uniform(0.0, 1.0)
        probFailure = random.uniform(0.0, 1.0)
        probFree = random.uniform(0.0, 1.0)
        probTsunami = random.uniform(0.0, 1.0)
        pid = os.getppid()
        if probVirus < 0.07 :
            os.kill(pid, signal.SIGPROF)
            print("#DEBUG CATACLYSM :: Virus has occured")
        if probFailure < 0.15 :
            os.kill(pid, signal.SIGUSR2)
            print("#DEBUG CATACLYSM :: Technical Failure has occured")
        if probFree < 0.01 :
            os.kill(pid, signal.SIGIOT)
            print("#DEBUG CATACLYSM :: Today is EnergyFree Day!!!")
        if probTsunami < 0.04 :
            os.kill(pid, signal.SIGWINCH)
            print("#DEBUG CATACLYSM :: Tsunami has occured")
        time.sleep(5)

