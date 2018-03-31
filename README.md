# Transcendence project [![Build Status](https://travis-ci.org/conformist-mw/37_transcendence_1.svg?branch=master)](https://travis-ci.org/conformist-mw/37_transcendence_1)

This project will be a social network for science targets. Available at [conformist.pp.ua](https://transcendence.conformist.pp.ua/)

# Installation Guide

First of all clone this project:

```bash
git clone https://github.com/conformist-mw/37_transcendence_1
```

Then install project requirements (better within [virutal environment](https://docs.python.org/3/tutorial/venv.html))

```bash
pip install -r requirements.txt
```

Create database and user:

```bash
sudo -i -u postgres
createuser transcendence -P
createdb transcendence -O transcendence
exit
```

Edit `.envs` file with your credentials and source it:

```bash
. .envs
```

Run migrate

```bash
make migrate
```

# How to run

Just simple:

```bash
make run
```


# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
