ptdk: Webserver to create tutorial skeleton from workflow
=========================================================

It uses Planemo to create the skeleton of a tutorial  for Galaxy Training Material from a public workflow on a public Galaxy instance.

# Usage

## Requirements

- Pip
- Virtualenv

## Prepare the environment

- Create virtual environment

    ```
    $ virtualenv -p python3 .venv
    ```

- Activate the environment

    ```
    $ . .venv/bin/activate
    ```

- Install the requirements

    ```
    $ pip install -r requirements.txt
    ```

## Start the server

- Start the server

    ````
    $ export FLASK_APP=ptdk
    $ export FLASK_ENV=development
    $ flask init-db
    $ flask run
    ```

## 

We use:

- Flask
- Planemo
- Bulma