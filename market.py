""" notes : il faudrait purchasingPow entre -5 et 5
            il faudrait que carbonPrice soit la différence entre le prix du carbone avant et maintenat
            il faudrait définir un prix de base (genre celui de la première itération)
            il faudrait que conso soit aussi une différence (comme ça si elle est négative le prix baisse et inversement)"""

# KWh Price : 0.16 €
from multiprocessing import Process
from queue import Queue

def energPriceChang(precedPrice, carbonPrice, purchasingPow, politic, isTechnicalFailure, isVirus, isFreeEnergyDay, isTsunami, conso):
    newPrice = precedPrice * (1 + conso * 0.001)
    if isFreeEnergyDay == true :
        newPrice = 0
    else :
        newPrice = newPrice + 0.02 * (carbonPrice + purchasingPow/10)
        if politic == true :
            newPrice = newPrice + 0.03
        if isTechnicalFailure == true :
            newPrice = newPrice + 0.015
        if isVirus == true :
            newPrice = newPrice + 0.02
        if isTsunami == true :
            newPrice = newPrice + 0.025

        print(newPrice)

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
    global isTechnicalFailure
    global isFreeEnergyDay
    global isTsunami
    global isVirus

    if sig == signal.SIGUSR1 :
        politic = True
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


def run():
    qEco = Queue()
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

    lockFailure = threading.Lock()
    lockVirus = threading.Lock()
    lockFree = threading.Lock()
    lockTsunami = threading.Lock()

    pCata = Process(target = cataclysme, args =(,))

    conso = 10 #à mettre en lien avec les homes

    p = Process(target = energPriceChang, args = (precedPrice, carbonPrice, purchasingPow, politic, isTechnicalFailure, isVirus, isFreeEnergyDay, isTsunami, conso,))
    p.start()
    p.join()
