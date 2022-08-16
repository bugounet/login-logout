# On pourrait prendre une alpine pour la légèreté
# mais la c'est pas très pertinent de me battre avec
# GCC pour un test technique.
# Aussi, je prends la version slim qui sera plus légère
# mais suffisament bien équipée pour embarquer des les lib
# de crypto usuelles.
# De même: faut pas run en root, donc je suis supposé créer
# un user non root pour faire tourner le code. Ce sera fait
# en prod' pas ici. ^^
FROM python:3.10-slim AS base
ARG POETRY_VERSION
ARG PG_USER
ARG PG_PWD
ARG PG_HOST
ARG PG_DATABASE

# je suis pas assez devops pour savoir si c'est mieux
# d'utiliser /code /app ou autre... je reste sur mes
# habitudes: dans ma vie on utilise beaucoup /app
WORKDIR /app

# Copier les requirements et lancer poetry pour
# installer tout le monde. La version de poetry est
# passée en build-arg.
RUN pip install poetry==$POETRY_VERSION
# pas besoin de créer les virtualenvs dans docker
RUN poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml /app/
# on pourrait ajouter/enlever les dev-deps en fonction d'un autre build-arg
RUN poetry install --no-interaction --no-ansi

# build à deux étages pour éviter de réinstaller poetry et
# les libs à chaque build. On peut faire mieux mais pour
# mon petit besoin ponctuel ça suffira amplement.
FROM base AS final
WORKDIR /app
COPY ./src/msio /app/msio
COPY ./alembic /app/alembic/
COPY ./alembic.ini /app/

CMD ["uvicorn", "msio.logme.__main__:app", "--reload", "--host", "0.0.0.0"]