# Welcome to CrowdReviews Django Repo

## This file will guide you through the installation of the project

### Please make sure you have the following technologies installed on your computer beforehand
1. [Python](https://www.python.org/downloads/) (Please make sure the version is 3.9 or above)
2. [Poetry](https://python-poetry.org/docs/)
3. [MySql with Workbench](https://dev.mysql.com/downloads/installer/)

### To Install this project, open it in pycharm and run the following command in the terminal

`poetry install`

This will install all the project dependencies.

#### Configure the pycharm interpreter to use the poetry environment.

### Now use the MySql Workbench and configure the Database schema

## Voila .... it is now time to run the server

# Make sure to run every command as displayed below

1. poetry run python manage.py makemigrations
2. poetry run python manage.py migrate
3. poetry run python manage.py runserver

# Follow the below commands to configure the dependencies

1. poetry add [dependency name]
2. poetry remove [dependency name]
3. poetry add [dependency name] --dev (For dev dependencies)

We can install the project for production using the following command:

`poetry install -no-dev`