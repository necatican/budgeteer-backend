# budgeteer-backend

### Getting the server up and running for development

#### Prerequisites

- [Poetry](https://python-poetry.org/docs/#installation)
- A PostgreSQL instance, this documentation uses [Podman](https://podman.io/getting-started/installation)

#### Deploying PostgreSQL and pgAdmin with Podman (Tested on MacOS)

Initialize required variables.

```
export PODMAN_VOLUME_PATH="$HOME/.podman-volumes"

export PG_USER='budgeteer'
export PG_PASSWORD='Ch4ngeM3'
export PG_PORT='5432'

export PG_ADMIN_EMAIL='test@test.com'
export PG_ADMIN_PASSWORD="$PG_PASSWORD"
export PG_ADMIN_PORT='9876'

```

Podman creates a VM to run pods. Create a machine with a persistent volume.

```
podman machine init --volume "$PODMAN_VOLUME_PATH" budgeteer-machine
podman machine start budgeteer-machine
```

We need a pod to run our containers. And volumes to keep our data _persistent_. We are binding the ports to access our containers externally.

Be careful. Binding 5432 might cause issues if you already have a PostgreSQL deployment.

```
podman pod create --name budgeteer-psql -p "$PG_ADMIN_PORT:80" -p "$PG_PORT:5432"
podman volume create psql
podman volume create pgadmin
```

Run the containers.

```
podman run --name pgadmin --pod budgeteer-psql \
    -e "PGADMIN_DEFAULT_EMAIL=$PG_ADMIN_EMAIL" \
    -e "PGADMIN_DEFAULT_PASSWORD=$PG_ADMIN_PASSWORD"  \
    -v pgadmin:/var/lib/pgadmin \
    -d docker.io/dpage/pgadmin4:latest

podman run --name psql --pod=budgeteer-psql -d \
    -e "POSTGRES_USER=$PG_USER" \
    -e "POSTGRES_PASSWORD=$PGPASSWORD" \
    -v psql:/var/lib/postgresql/data \
    docker.io/library/postgres:15

```

If everything went according to the plan, you now have a PostgreSQL installation with pgAdmin

- pgAdmin UI: <http://localhost:$PG_ADMIN_PORT>

#### Deployment

- Clone this repository
- Run `poetry install` to install all the dependencies in a virtual environment.
  - You can either use your tool commands with poetry or activate the poetry shell with `poetry shell`.
  - If you are using VSCode; you should [change your interpreter](https://code.visualstudio.com/docs/python/environments#_work-with-python-interpreters). To get the poetry interpreter path; simply run `poetry env info --path`
- Create a `.env` file and fill in the variables.
  - `cp .env.sample .env`
- Run the migrations with Alembic.
  - You may need to create a PostgreSQL database.
  - `poetry alembic upgrade heads`
- Run the server with uvicorn
  - `poetry run uvicorn app.main:app --reload`
