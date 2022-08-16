# découverte du sujet

Hello, tu trouveras dans le dossier
doc, le fruit de mon raisonnement,
les étapes par lesquelles je suis passé
et les choix j'ai fait et surtout quelles
questions j'ai essayé de résoudre.

Le sujet que tu m'as transmis:
À partir de la base de code fournie:
1. créer un utilisateur
2. Avoir une route pour se connecter/déconnecter
3. avoir des routes pour les opérations de base
(create, update, read, delete)

## Premiers pas

J'ai pris le temps de regarder le code que tu
m'as envoyé, comment il est découpé, s'il y a des
commentaires comme des TODO, des FIXME ou autre.

À cette lecture, je vois le `pyproject.toml` qui
pointe vers un python3.10 (merci) mais aussi 
sqlalchemy, fastapi et quelques autres dépendances.

Je suis suis pas à l'aise avec sqlalchemy mais
ce test technique va me permettre de m'y frotter
et de découvrir celui-ci.

Le dossier tests contient un simple test 
qui vérifie que le nom de projet peut être
chargé depuis les vars d'env. C'est pas exhaustif
et pour le coup je suppose que c'est plus pour 
aiguiller sur l'emplacement espéré des tests que
pour vraiment tester le boostrap que tu m'as 
envoyé.

J'ai pour habitude de bosser avec du TDD, donc
j'envisage déjà d'aller ajouter hypothesis et 
ou factoryboy pour m'outiller un peu plus dans
l'écriture des tests.

Tu fournis le modèle SQL Alchemy qui stocke
les utilisateurs. C'est ça de pris. Je sais 
quelles infos je vais utiliser.

Tres près des modèles, je vois que tu m'offre
les schémas de l'API (User, AccessToken). Je
vois aussi que tu as créé un router fastAPI 
que où tu as déjà pris le temps de supprimer
tes vues. À défaut de me fournir une convention
pour les endpoints API, j'ai le format des données,
et ca me guide sur les noms des classes. :]

Le main contient l'init de l'appli, mais aussi
des vues bateau. Je vais les appeler vite fait
à coups de curl pour vérifier que j'ai bien
réussi mon setup, cependant ça fait du bruit 
dans le code et ça ne sert pas au sujet. Je vais
les virer dès que mon environnement sera 
opérationnel.

## plan d'attaque

Je découpe le sujet vite fait en grosse mailles
pour m'ograniser un peu. Je pense partir du 
skelette que tu m'as envoyé car tout refaire
moi même n'apportera rien de révolutionnaire.

Donc pour commencer, je pense que je vais faire ça:

1. Setup l'environnement et faire tourner le 
bootstrap

Rien de fou là dedans, juste ce qu'il faut pour 
avoir un environnement qui boot

2. Créer un utilisateur via command-line

Pour créer un utilisateur, mon API n'existant
pas, je suppose que je vais avoir besoin d'une
fixture ou d'une fonction en CLI pour faire
ce travail. Il y a deux vars d'env dans la config:
FIRST_USER_EMAIL et FIRST_USER_PASSWORD. 
Je me baserai dessus pour créer l'utilisateur
au boot du server.

3. Recréer les endpoints que tu as retiré

Je vais faire déjà deux endpoints: /v1/login et
/v1/logout. Faura pendre le temps de choisir le
verbe, le format des paramètres, les codes
attendus. Je documenterai tout ça plus loin
dans la doc. Faudra aussi que je mette un peu
de sécurité (du throttling?)

4. (pas sûr, on verra) Ajouter des tests pour sécuriser le bootstrap
que tu m'as envoyé

5. réaliser le CRUD

Là encore, rien de révolutionnaire,
on veut pouvoir lire mon user, 
changer son nom/prénom, le supprimer, lui créer
des copains. J'ai pas d'info, je vais
mettre une seule contrainte sur ces appels:
seul l'utilisateur initial pourra faire ces
actions. Vu que je suis pas sûr de cette règle,
je vais m'arranger pour qu'elle soit facilement 
remplaçable.

6. un peu de nettoyage

A la fin, je prendrai du temps pour peaufiner
le swagger, créer une collection postman
pour avoir une suite de tests e2e et un README
pour que tu puisse réinstaller le projet que je te
renvoie. Vu que tu m'envoie le sujet sous forme
d'archive, je pense pas que tu veuille que je 
t'upload ça dans un repo privé sur github.

Je vais me permettre un petit git init histoire 
que tu puisse jeter un oeil au gitlog en local
si le coeur t'en dit. En fonction de ta réponse,
je mettrai mon .git ou pas dans l'archive.

Attaquons avec le [setup](02-setup.md)