# creation du premier utilisateur

Afin de toujours l'avoir à dispo, je prends
le parti de charger mes fixtures au boot
de fastapi. C'est pas très efficient car si on
est en prod', à chaque reboot du conteneur 
ça me fait taper sur postgres pour verifier
que mon first-user est bien là, néanmoins
c'est plus simple que de créer un service
docker-compose qui vient migrer et synchroniser
les fixtures.

Dans l'implémentation il est nécessaire de 
stocker le mot de passe de l'utilisateur.
Il faut être malin ici: je vais stocker un hash.
J'aurais pû aller loin car l'OWASP propose
d'utiliser l'algorithme Argon2 pour protéger
au mieux la base des attaques par bruteforce,
néanmoins c'est pas de base dans hashlib, donc
je vais me contenter de concaténer le secret de
l'appli avec le mot de passe, puis de stocker 
le sha256 de cette concaténation.

Cet algo naïf permet d'avoir des passwords protégés
par le secret de l'appli et ça dépanne à défaut d'utiliser
Argon.

Pour le username, je n'ai aucune info ou contrainte
d'unicité. Je vais donc me contenter de le prendre
sur les inputs du client. Dans ma fixture il
s'appellera "first-user".

Le code commençant à grossir, je me rends compte
qu'il me manque un petit linter à tout cet
environnement. J'ajoute donc black, flake8 et
isort à mes outils.

[Implémenter le CRUD](04-Implementer-le-CRUD.md)
