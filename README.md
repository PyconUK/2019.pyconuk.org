# PyCon UK Website 2019
This is the repo for [PyCon UK 2019's website](http://2019.pyconuk.org).

It consolidates multiple systems into one code base.

Many people committed their time and effort to the precursor projects.
However we would like to specially thank the following people:

* Kirk Northrop
* Owen Campbell
* Peter Inglesby
* Vincent Knight


## Install

    make setup

This project uses [Pipenv](https://pipenv.readthedocs.io/en/latest/) to handle dependency installation and pinning, you will need it installed to install the requirements.
We recommend installing it with [pipsi](https://github.com/mitsuhiko/pipsi).


## Running
The following command is the fastest way to get up and running:

    make run


Note: this project relies on environment variables locally to run.
A `.envrc` exists for use with [direnv](https://direnv.net/) (which will also run `pipenv shell` for you).
