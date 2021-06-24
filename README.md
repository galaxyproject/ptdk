ptdk: Web server to create tutorial skeleton from workflow
==========================================================

[![CircleCI](https://circleci.com/gh/bebatut/ptdk/tree/master.svg?style=svg)](https://circleci.com/gh/bebatut/ptdk/tree/master)

It uses Planemo to create the skeleton of a tutorial  for Galaxy Training Material from a public workflow on a public Galaxy instance.

# Usage

## Requirement

- virtualenv

## Prepare the environment

- Create virtual environment:

    ```
    $ make create-venv
    ```

## Run the server

- Initiate the database (once):

    ```
    $ make init-db
    ```

- Export the API for usegalaxy.eu, usegalaxy.org.au and usegalaxy.org.au as environment variables:

    ```
    $ export USEGALAXY_EU_APIKEY=<replace with correct API key>
    $ export USEGALAXY_ORG_AU_APIKEY=<replace with correct API key>
    $ export USEGALAXY_ORG_APIKEY=<replace with correct API key>
    ```

- Launch the server: 

    ```
    $ make run
    ```

- Browse it at [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
- Kill it with CTRL+C

## Run the tests

- Install the requirements: 

    ```
    $ make setup
    ```

- Run the tests: 

    ```
    $ make test
    ```

## Deploy to Heroku (https://ptdk.herokuapp.com/)

Automatically done when push to master

# How is it working?

It uses:

- [Flask](http://flask.pocoo.org/docs/1.0/) for the web server
- [Planemo](https://planemo.readthedocs.io/en/latest/) to generate the skeleton from a workflow
- [Bulma](https://bulma.io/) to make it nice looking

# Contributing

Please check the [`CONTRIBUTING`](CONTRIBUTING.md) file for details

# Code of Conduct

Please note that this project is released with a Code of Conduct. By participating in this project you agree to abide by its terms. See the [CODE_OF_CONDUCT](CODE_OF_CONDUCT) file.

# License

ptdk is released under the MIT License. See the bundled [`LICENSE`](LICENSE) file for details.