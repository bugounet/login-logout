# Login logout API demo

Ceci est un test technique montant une petite api qui propose 8 endpoints:
- login
- logout
- create user
- update user
- delete user
- list user
- get user details
- healthcheck


**disclaimer**

Ceci n'est en aucun cas un code utilisable en 
production. Trop de choix techniques ont été 
faits pour répondre au sujet du test en un 
temps raisonnable ce qui amène des failles 
critiques de sécurité.

Le carnet de bord du test technique se trouve [ici](docs/01-discovery.md)

# Running instructions

Run and build the project using docker compose.

```shell
# create your .env file
cp docker/.env.dist  docker/.env
vim docker/.env
# run docker
 docker compose -f docker/docker-compose.yml up --build
```

open [http://localhost:8000/docs](http://localhost:8000/docs)
to get the swagger of the project.