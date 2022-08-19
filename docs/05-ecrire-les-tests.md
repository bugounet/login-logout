# Rediger des tests

Mon but c'est: pouvoir avoir une preuve que
le programme marche. J'ai donc pris le temps
de créer des tests.
J'ai commencé par le domaine car il vit très bien
et que c'est presque du python pur. Puis j'ai écrit
les tests qui vont autour.

Pendant l'écriture de ces tests, j'ai fait un peu
de refacto pour supprimer ce qui ne me sert pas
dans le bootstrap project, et pour re-ranger
certaines classes.

J'ai aussi fait le choix d'intégrer les schémas 
au domaine. C'est une pratique discutable car 
idéalement je ne dois pas me marier à une techno
pour coder mon domaine, néanmoins pydantic
est un outil tellement utile, qu'il mériterait
de faire partie du langage. J'accepte de faire
cette concession :P

Apres une soirée à rédiger les tests, j'arrive à 
un coverage de 80% du code. J'aurais aimé y 
passer plus de temps, mais il faut être pragmatique,
toucher le 100% ne se fera pas en 2 minutes.

Petit hack: Pour faciliter mon test, avoir des 
bonnes perfs et parce que mes requêtes sont
simples, j'ai préféré utiliser une base de donnée 
sqlite en RAM pour faire tourner la suite de tests.

Pas de chance, cette pratique a échoué: j'ai vu qu'en
lançant la suite complète, les tests ne sont pas 
indépendants et la fixture n'arrive visiblement
pas à recréer le jeu de données entre chaque test. 
Tant pis... ça m'apprendra à vouloir hacker. 😛
 
J'aurais dû aller brancher une vrai instance postgres.
J'ai gaspillé mon temps, et le système ne me permet pas de
prouver que mon code marche car je suis pas ISO avec le runtime.

Petite zone que j'ai laissée non testée: l'api
fast-api. J'aurais dû jouer de l'injection de
dépendance pour fournir à fast-api les bons
repositories pour ne pas tester l'ORM en meme 
temps que je vérifie que fast API est bien branché.

Contrairement à ce que je pensais en intro: le sujet est
straighforward. Je n'ai pas eu de business rules complexes
à implémenter. J'ai donc pas eu besoin de brancher factoryboy
ou hypothesis.

[--> conclusions](06-conclusions.md)
