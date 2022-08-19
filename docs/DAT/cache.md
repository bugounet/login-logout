# Cache management

17 Aout 2022
`Variable thread local`

Le cache permet de stocker de la donnée volatile
de façon rapide. La perte des données en cache ne
doit pas empêcher le fonctionnement de l'appli.

Dans le cas du stockage des tokens générés par
l'application, j'ai eu besoin de garder une table
de correspondance entre les tokens et les
utilisateurs.

## Choix considérés
- redis
- memcached
- une zone memoire

Redis et Memcached ont été écartés car le setup
de ces outils et l'import des libs représentait
un investissement en temps considérable.

## Solution retenue

Une variable locale au Thread de l'appli
qui stocke les tokens.

## Limites

Aucun contrôle n'est fait sur la taille de
ce mapping. Si plusieurs serveurs d'API tournent
en parallèle, ce système ne sera plus suffisant.