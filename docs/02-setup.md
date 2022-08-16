# Setup de l'env et premiers fixs

Merci pour le fichier toml, ça aide. J'installe
tout, je configure mon EDI. Premiere 
surprise : les tests fournis ne tournent pas.

![Le premier run échoue](images/premier-run-des-tests.png)

Il s'agissait d'une coquille dans le test. (un 
copié-collé ?)

Quelques petites autres surprises comme la casse
de PROJECT_NAME qui n'était pas bonne entre 
la config et le `main`. Après ces petits fixs 
j'arrive à mes fins :
Le `hello world` est opérationnel et tous 
les tests passent.

![le hello world](images/hello-world.png)

![les logs de l'appli](images/logs-hello-world.png)

![les tests sont au vert](images/tests-ok.png)

Il me manque un dernier truc dans mon setup:
une base de données.  

Il va me falloir une instance PG. Je n'ai pas
envie de souiller mon ordi, donc je vais le
mettre dans un conteneur docker. J'en profite
pour te remettre le `docker-compose.yml`. 
Rien de fou, je mets 2 services, PG et l'API.

Me voilà parti pour créer mes 
`Dockerfile`, `docker-compose.yml` et 
`.Dockerignore`. 

Je fige une version de poetry
dans les build-args pour éviter les 
évolutions cassantes, mais pouvoir me 
mettre à jour.

Je préfère éviter de télécharger poetry 
à coups de `curl | python` dans le conteneur 
docker : on ne sait jamais ce qu'on va
récupérer. Ce sera `pip install` pour moi.

J'exploite les variables d'env prévues dans le
fichier `config.py`.

_note pour plus tard: penser à documenter 
les vars d'env pour ceux qui vont déployer
ça en prod'_

Si tu veux jouer avec, voici les commandes pour
build l'image manuellement, run un conteneur
ou lancer tout le docker-compose:

```shell
docker build --build-arg POETRY_VERSION=1.1.14 -f ./docker/Dockerfile -t api .
docker run -p 8000:8000 --env-file ./docker/.env api
docker compose -f docker/docker-compose.yml up --build
```

Mon docker-compose.yml étant créé, je me rends
compte qu'il faut former la DB. pour ça 
il y a Alembic, qui va me permettre de créer
des "migrations" de schéma. Il n'est pas dans
le `pyproject.toml`. Je l'ajoute.

J'ajoute alembic, et psycopg2-binary pour
pouvoir run mes migrations.

Temps passé sur cette étape :
environ 2h principalement parce que j'ai
rencontré un petit pépin sur le healthcheck,
j'ai donc retiré cette option de mon 
`docker-compose.yml` pour pas rester coincé.

Passons à la suite:
[créer le premier utilisateur](03-creer-first-user.md)
