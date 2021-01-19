# PPC_The_Energy_Market

##Sommaire
	I) Objectifs du projet
	II) Exécution
	III) Description des fichiers

## I) Objectifs du projet 
- concevoir est implémenter une simulation multi-processus et multi-thread en python
- simuler un marché d'énergie prenant en compte :
	- la production et la consommation des maisons
	- la météo
	- l'évolution du prix 
	- l'économie
	- la politique 
	- des évènements inattendus

## II) Exécution 
Dans un terminal : python3 main.py

## III) Description des fichiers

**weather**
Thread qui définit la température et le nombre d'heures d'ensoleillement dans la journée.
Modifie la consommation et la production d'énergie des homes grâce à une shared memory.

**homes**
Multi-thread (un thread par home), chaque home produit et consomme de l'énergie en fonction de weather.
Certaines homes vendent leur surplus de production au marché, et d'autres le donne à d'autres homes. (message-queue entre les homes)
Pour récupérer de l'énergie ou en vendre les homes communiquent avec le market par message-queue.

**market**
Contient le market (processus) ainsi que economics, politics et cataclysme (ses processus fils)
- politics :
	Permet de savoir si on est en guerre, auquel cas la prix du kWh augmente.
	Communique avec market avec un signal (true = en guerre)
- economics : 
	Influence le prix du kWh en fonction du prix du carbonne et des fluctuations du pouvoir d'achat
	Communique avec market avec une shared memory
- cataclysme :
	évènements à faible probabilité d'apparition qui influencent le prix du kWh
	Evenements : défaillance technique, Virus, Tsunami (augmentent le prix à différents niveaux), Free Energy Day (énergie gratuite pendant un jour)
	communique avec market avec des signaux (un par évènement)

**main**
Fichier permettant de créer les message-queues (entre homes et market) et la shared-memory (entre weather et homes).
Il permet de lancer homes, weather et market.

