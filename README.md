[![CircleCI](https://circleci.com/gh/kmazi/flight-book.svg?style=svg)](https://circleci.com/gh/kmazi/flight-book)

# Flight-book
An application for booking flights to a given destination.

# Table of Content
- [Flight-book](#flight-book)
- [Table of Content](#table-of-content)
- [Project Structure](#project-structure)
- [Setup](#setup)
- [Author](#author)

# Project Structure
```bash
├── user
│   ├── migrations
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── app
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── user
│   ├── migrations
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── .env
├── .gitignore
├── .python-version
├── factories.py
├── LICENSE
├── manage.py
├── Pipfile
├── Pipfile.lock
└── README.md
```

# Setup
 - Run `git clone https://github.com/kmazi/flight-book.git` to clone the project locally.
 - Create a local postgres database locally and add it's url to the DATBASE_URL env variable.
 - In your terminal, navigate to the project directory and spin up a pipenv shell via `pipenv shell`. If you don't already pipenv you can install it via pip install pipenv
 - Run `pipenv install --dev` to install all project dependencies.
 - Run migration with `python manage.py migrate`.
 - Start the app with `python manage.py runserver`

# Author
This software was created by Mazi Ugochukwu, a Python and C# programmer