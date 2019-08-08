ptdk: Web server to create tutorial skeleton from workflow
==========================================================

It uses Planemo to create the skeleton of a tutorial  for Galaxy Training Material from a public workflow on a public Galaxy instance.

# Usage

## Prepare the environment

- Create virtual environment: `make create-venv`

## Run the server

- Initiate the database (once): `make init-db`
- Launch the server: `make run`
- Browse it at [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
- Kill it with CTRL+C

## Run the tests

- Install the requirements: `make setup`
- Run the tests: `make test`

# How is it working?

It uses:

- [Flask](http://flask.pocoo.org/docs/1.0/) for the web server
- [Planemo](https://planemo.readthedocs.io/en/latest/) to generate the skeleton from a workflow
- [Bulma](https://bulma.io/) to make it nice looking