import random
import threading

def run (temp, weatherSM, barrier):
    print("#DEBUG WEATHER :: Starting weather")
    day = 0
    while True : 
        #définition de la température
        temp = random.uniform((temp-5.0), (temp+5.0))
        if temp < -10.0 :
            temp = -10.0
        elif temp > 45.0 :
            temp = 45.0

        #définition de l'ensoleillement
        ensol = random.uniform(0.0, 12.2)
        print("#DEBUG WEATHER :: Day %d | temp : %.2f | ensol : %.2f" % (day, temp, ensol))
        weatherSM[0]=temp
        weatherSM[1]=ensol

        day += 1
        barrier.wait()


