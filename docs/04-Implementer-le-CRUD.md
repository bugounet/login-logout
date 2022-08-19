# Recréer les endpoints que tu as supprimé

Pour implémenter ce CRUD, je choisis de partir
sur une implémentation en clean architecture.
Cette architecture va me permettre de décorréler
le domaine (actions qu'on va pouvoir faire
sur les utilisateurs) de leur implémentation
concrète.

Je crée donc une interface UserRepository qui
me permet d'inverser la dépendance entre mon
domaine et la base de données. 
Faire ce travail permet de commencer à réléchir
aux actions que je vais faire sur ma base
de données. J'y vois pour le moment 6 actions:
- trouver un utilisateur à partir de ses credentials
- trouver un utilisateur à partir de son email
- trouver un utilisateur à partir de son ID
- lister tous les utilisateurs (pas de filtre)
- créer un nouvel utilisateur
- supprimer un utilisateur

La logique métier va se trouver dans les use-cases
ainsi que dans les entités. Exemple : le calcul
du hash des mots de passe des utilisateurs
va être rangée dans l'entité utilisateur
tandis que la désactivation des tokens de l'utilisateur
lorsqu'il change de mot de passe sera plutôt côté 
use-case.

Premier résultat : j'ai ma fonction de login sans
faire beaucoup d'efforts sur sa documentation
dans swagger...

![requete de login dans swagger](images/login-request.png)

![verification du token](images/token-verification.png)

Je procède ainsi jusqu'à avoir les endpoints
- login
- logout
- les 4 routes de CRUD sur l'utilisateur

Pour que le logout soit fonctionnel, je dois
garder en mémoire la liste des tokens générés 
pour pouvoir se déconnecter. J'ai vu dans le 
sample que tu avais utilisé redis.

Vu que je ne suis pas en plein weekend, j'ai
moins de temps. Je me contente d'un dict en thread
local. Malgré ce choix, j'ai quand même l'interface
prête à être swapped pour du redis si on change
d'avis parce que j'ai écrit une abstraction de 
l'interface.

[--> ecriture des tests](05-ecrire-les-tests.md)