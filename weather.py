import random
import threading

def changementTemp (tempPreced):
    print("Starting thread:", threading.current_thread().name)
    #définition de la température
    temp = random.uniform((tempPreced-5.0), (tempPreced+5.0))
    if temp < -10.0 :
        temp = -10.0
    elif temp > 45.0 :
        temp = 45.0

    #définition de l'ensoleillement
    ensol = random.uniform(0.0, 12.2)

    print("Ending thread:", threading.current_thread().name)


if __name__ == "__main__":
    tempAct = 20.0
    print("Starting thread:", threading.current_thread().name)
    thread = threading.Thread(target=changementTemp, args=(tempAct,))
    thread.start()
    thread.join()
