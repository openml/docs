# Installation

*Current instructions tested on Mac, but likely work on most Unix systems.*

The OpenML server will be developed and maintained for the latest minor release of
Python (Python 3.12 as of writing).
You can install the dependencies locally or work with docker containers.

??? tip "Use `pyenv` to manage Python installations"

    We recommend using [`pyenv`](https://github.com/pyenv/pyenv) if you are working with
    multiple local Python versions. After following the installation instructions for
    `pyenv` check that you can execute it:

    ```text
    > pyenv local
    3.12
    ```

    If `pyenv` can't be found, please make sure to update the terminal environment
    (either by `reset`ing it, or by closing and opening the terminal). If you get the message
    `pyenv: no local version configured for this directory` first clone the repository
    as described below and try again from the root of the cloned repository.

    You can then install the Python version this project uses with:
    `cat .python-version | pyenv install`


## Local Installation

These instructions assume [Python 3.12](https://www.python.org/downloads/)
and [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) are already installed.

!!! info "You may need to install Python3 and MySQL development headers."

    It may be necessary to first install additional headers before proceeding with a
    local installation of the `mysqlclient` dependency. They are documented under
    ["Installation"](https://github.com/PyMySQL/mysqlclient#linux) of the `mysqlclient`
    documentation.

=== "For Users"

    If you don't plan to make code changes, you can install directly from Github.
    We recommend to install the OpenML server and its dependencies into a new virtual
    environment.
    ```bash  title="Installing the project into a new virtual environment"
    python -m venv venv
    source venv/bin/activate

    python -m pip install git+https://github.com/openml/server-api.git
    ```
    If you do plan to make code changes, we recommend you follow the instructions
    under the "For Contributors" tab, even if you do not plan to contribute your
    changes back into the project.


=== "For Contributors"

    If you plan to make changes to this project, it will be useful to install
    the project from a cloned fork. To fork the project, go to our
    [project page](https://github.com/openml/server-api) and click "fork".
    This makes a copy of the repository under your own Github account.
    You can then clone your own fork (replace `USER_NAME` with your Github username):

    ```bash title="Cloning your fork"
    git clone https://github.com/USER_NAME/server-api.git
    cd server-api
    ```

    Then we can install the project into a new virtual environment in edit mode:

    ```bash title="Installing the project into a new virtual environment"
    python -m venv venv
    source venv/bin/activate

    python -m pip install -e ".[dev,docs]"
    ```
    Note that this also installs optional dependencies for development and documentation
    tools. We require this for contributors, but we also highly recommend it anyone
    that plans to make code changes.

## Setting up a Database Server
Depending on your use of the server, there are multiple ways to set up your own
OpenML database. To simply connect to an existing database, see
[configuring the REST API Server](#configuring-the-rest-api-server) below.


### Setting up a new database
This sets up an entirely empty database with the expected OpenML tables in place.
This is intended for new deployments of OpenML, for example to host a private OpenML
server.

!!! Failure ""

    Instructions are incomplete. See [issue#78](https://github.com/openml/server-api/issues/78).

### Setting up a test database

We provide a prebuilt docker image that already contains test data.

=== "Docker Compose"
    To start the database through `docker compose`, run:

    ```bash
    docker compose up database
    ```

    which starts a database.

=== "Docker Run"

    To start a test database as stand-alone container, run:

    ```bash
    docker run  --rm -e MYSQL_ROOT_PASSWORD=ok -p 3306:3306 -d --name openml-test-database openml/test-database:latest
    ```

    You may opt to add the container to a network instead, to make it reachable
    from other docker containers:

    ```bash
    docker network create openml
    docker run  --rm -e MYSQL_ROOT_PASSWORD=ok -p 3306:3306 -d --name openml-test-database --network openml openml/test-database:latest
    ```

The container may take a minute to initialise, but afterwards you can connect to it.
Either from a local `mysql` client at `127.0.0.1:3306` or from a docker container
on the same network. For example:

```bash
docker run --network NETWORK --rm -it mysql mysql -hopenml-test-database -uroot -pok
```
where `NETWORK` is `openml` when using `docker run` when following the example,
and `NETWORK` is `server-api_default` if you used `docker compose` (specifically,
it is `DIRECTORY_NAME` + `_default`, so if you renamed the `server-api` directory to
something else, the network name reflects that).

## Configuring the REST API Server

The REST API is configured through a [TOML](https://toml.io) file.

!!! Failure ""

    Instructions are incomplete. Please have patience while we are adding more documentation.
