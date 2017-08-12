[![Coverage Status](https://coveralls.io/repos/github/charlieoduk/Bucketlist/badge.svg?branch=develop)](https://coveralls.io/github/charlieoduk/Bucketlist?branch=develop)
[![Build Status](https://travis-ci.org/charlieoduk/Bucketlist.svg?branch=develop)](https://travis-ci.org/charlieoduk/Bucketlist)
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/hyperium/hyper/master/LICENSE)

# Bucket List API
![](http://i.imgur.com/fMC47f1.jpg)

### Overview

A bucketlist defined as a list of things a person would like to accomplish during their lifetime.

The bucketlist API is a RESTful API that provides various endpoints that make it easy to perform CRUD operations on 
bucketlists as well as their 
constituent bucketlist items.

#### Language
This API is written in `Python 3.6` making use of the Flask Micro-framework and Flask Restplus. It's documentation is 
done using Sphinx. 

#### Database
We shall be using `Postgres` for storage of all the app data

### Installation and Setup
1. Clone the repository from Github
```commandline
$ git clone https://github.com/charlieoduk/Bucketlist
```
2. Cd into the working directory
```commandline
$ cd Bucketlist
```
3. Create a virtual environment and activate it. If you don't have virtualenv, install it using `pip install virtualenv` 
then run the commands below.
```commandline
$ virtualenv venv
$ source venv/bin/activate
```
4. Install the applications dependencies
```commandline
$ pip install -r requirements.txt
```

#### Database setup
If you don't already have Postgres installed, set it up on your machine (globally) by running the command below
```commandline
$ brew install potgresql
```
Let's get started setting up your database
1. Start Postgres
```commandline
$ psql postgres
```
2. Create the database
```commandline
$ createdb bucketlist
$ createdb bucketlist_test
```

#### Run Database migrations
```commandline
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade
```

You're all setup now, run the application using the command below
```commandline
$ python manage.py runserver
```
If everything is working, you should get the output below after running the command
```commandline
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 268-923-532
```

### Supported Endpoints


| URL Endpoint | HTTP Methods | Action |
| -------- | ------------- | --------- |
| `/auth/register/` | `POST`  | Register a new user|
|  `/auth/login/` | `POST` | Login user and receive token|
| `/bucketlists/` | `POST` | Create a new Bucketlist |
| `/bucketlists/` | `GET` | Retrieve all bucketlists belonging to a user |
| `/bucketlists/?page=1&per_page=20/` | `GET` | Retrieve 20 bucketlists per page |
 `/bucketlists/?q=name/` | `GET` | Search for a bucketlist by it's name|
| `/bucketlists/<id>/` | `GET` |  Retrieve a bucketlist by ID|
| `/bucketlists/<id>/` | `PUT` | Update a bucketlist |
| `/bucketlists/<id>/` | `DELETE` | Delete a bucketlist |
| `/bucketlists/<id>/items/` | `POST` |  Create items in a bucketlist |
| `/bucketlists/<id>/items/<item_id>/` | `DELETE`| Delete an item from a bucketlist|
| `/bucketlists/<id>/items/<item_id>/` | `PUT`| Update a bucketlist item's details|

### Running tests
```commandline
nosetests --cover-package=bucketlist --with-coverage
```
