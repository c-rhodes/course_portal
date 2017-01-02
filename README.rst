Enterprise Programming Assignment
=================================

Web service for course information

This project is deployed on Heroku and can be accessed with this url: https://lit-anchorage-84265.herokuapp.com/

The following instructions detail how to get this project running locally and how to deploy it to Heroku.


Running Locally (Tested on Ubuntu 16.04)
----------------------------------------

Download and install the following:

* `Python 3`_
* `Postgresql`_
* `virtualenvwrapper`_

.. _`Python 3`: https://www.python.org/downloads/
.. _Postgresql: https://www.postgresql.org/download/
.. _virtualenvwrapper: https://virtualenvwrapper.readthedocs.io/en/latest/

Create postgres database::

    $ sudo su - postgres -c "psql"
    postgres=# CREATE DATABASE course_portal OWNER cullenrhodes encoding 'utf8';
    
Create virtualenv::

    $ mkvirtualenv -p $(which python3) course_portal

Install dependencies::

    $ pip install -r requirements/local.txt

Run migrations::
    
    $ ./manage.py migrate
    
Create superuser via command line (Optional)::

    $ ./manage.py createsuperuser

Run server::
    
    $ ./manage.py runserver
    
The project should now be running at **localhost:8000**

Deployment
----------

The following details how to deploy this application.


Heroku
^^^^^^

`Install Heroku Toolbelt`_

Deploy to Heroku with the following commands::

    heroku create --buildpack https://github.com/heroku/heroku-buildpack-python

    heroku addons:create heroku-postgresql:hobby-dev

    heroku config:set DJANGO_ADMIN_URL="$(openssl rand -base64 32)"
    heroku config:set DJANGO_SECRET_KEY="$(openssl rand -base64 64)"
    heroku config:set DJANGO_SETTINGS_MODULE='config.settings.production'
    heroku config:set DJANGO_ALLOWED_HOSTS='.herokuapp.com'

    heroku config:set DJANGO_MAILGUN_SERVER_NAME=sandboxb7de56698df443608af1bb4d7364d354.mailgun.org
    heroku config:set DJANGO_MAILGUN_API_KEY=key-328f4f3aecd8c8ac97ebb040c5cd145a
    heroku config:set MAILGUN_SENDER_DOMAIN=lit-anchorage-84265


    heroku config:set PYTHONHASHSEED=random
    heroku config:set DJANGO_ADMIN_URL=\^admin/


    git push heroku master
    heroku run python manage.py migrate
    heroku run python manage.py check --deploy
    heroku run python manage.py createsuperuser
    heroku open

.. _`Install Heroku Toolbelt`: https://devcenter.heroku.com/articles/heroku-cli

Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html
