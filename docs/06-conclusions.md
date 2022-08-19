# Conclusions

Le sujet me demandait de faire un système de login/logout avec CRUD
sur les utilisateurs. J'ai choisi d'approcher ce test de ma même 
façon qu'une user story que je coderais en DDD. J'ai donc
pris le temps de créer tout le domaine puis de brancher les 
routes fast API par-dessus.

Ce test technique m'a bien plu. J'ai pris le temps de 
découvrir sqlalchemy, et de découvrir des fonctions que j'ignorais 
dans fastapi. J'ai quand même le regret de ne pas avoir pu
aller jusqu'au bout, j'avais bien plus d'idées que de temps.

Ce que j'ai fait et qui serait à revoir:

- hasher les mots de passes en SHA256 (il y a clairement mieux)
- Ne quasiment rien mettre dans les tokens JWT. Pas même de dates.
- Laisser les tokens dans une zone memoire plutôt que d'utiliser redis
- Tester avec une base SQLite au lieu de postgres
- Le workflow de login qui ressemble au flow "Client credentials"
or ce workflow est faible en termes de sécurité
- Le chargement des fixtures devrait être fait par le service docker
qui joue les commandes alembic.

Ce qui m'a rendu la tâche difficile au delà du temps, ça a été 
d'apprendre l'API de SQL alchemy en commençant par une AsyncSession.

Quelques suggestions d'évolutions du service:
Si je reprends ce service, en plus de corriger les points au dessus
je pense que je mettrais du throttling avec un sceau à jetons
pour découpler l'approvisionnement de la consommation et pouvoir
changer l'algo d'approvisionnement facilement.

Je pense que le chiffrement devrait être fait avec des algorithmes
plus sophistiqués.

Les conteneurs docker devraient être revus pour tourner en non root
et le port 5432 de postgres ,e devrait pas être ouvert à l'extérieur.

Le système ne gère qu'un seul admin, il faudrait qu'on puisse en
avoir plusieurs et que les tokens puissent être scopés. bref...
La liste est longue.

Merci pour la lecture et pour le sujet 👍
