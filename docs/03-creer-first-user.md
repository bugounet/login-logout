# creation du premier utilisateur

Afin de toujours l'avoir à dispo, je prends
la parti de charger mes fixtures au boot
de fastapi. C'est pas très efficient car si on
est en prod', à chaque reboot du conteneur 
ça me fait taper sur postgres pour verifier
que mon first-user est bien là, néanmoins
c'est plus simple que de créer un service
docker-compose qui vient migrer et synchroniser
les fixtures.

Trouver l'utilisateur et le créer s'il n'existe
pas sont des fonctions CRUD. Ca tombe bien, 
j'avais prévu d'en câbler un paire.
