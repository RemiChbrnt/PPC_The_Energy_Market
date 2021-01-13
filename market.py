""" notes : il faudrait purchasingPow entre -5 et 5
            il faudrait que carbonPrice soit la différence entre le prix du carbone avant et maintenat
            il faudrait définir un prix de base (genre celui de la première itération)
            il faudrait que conso soit aussi une différence (comme ça si elle est négative le prix baisse et inversement)"""
from multiprocessing import Process

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


if __name__ == "__main__":
    carbonPrice =
    purchasingPow =
    politic =
    isTechnicalFailure =
    isVirus =
    isFreeEnergyDay =
    isTsunami =
    conso =
    p = Process(target = energPriceChang, args = (precedPrice, carbonPrice, purchasingPow, politic, isTechnicalFailure, isVirus, isFreeEnergyDay, isTsunami, conso,))
    p.start()
    p.join()