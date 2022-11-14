# Grunge Rock Development Application

## Overview

This Django project implements a catalogue of Grunge rock music.  It has a fully-functional Django admin interface, and a read-only REST API.  It contains three related data models:

1. `Artist`
2. `Album`
3. `Track`
4. `Playlist`




#### Fork this repository

When you have completed the goals then you can open a Pull Request to this main repository.

### Set up a virtualenv

```shell
$ python3 -m venv venv
$ source venv/bin/activate
```

### Install dependencies

```shell
$ pip install --upgrade pip
$ pip install --requirement=requirements.txt
```

### Initialize the development database

```shell
$ python manage.py migrate
$ python manage.py loaddata initial_data
```

### Add a development superuser

```shell
$ python manage.py createsuperuser
```

### Run the development server

```shell
$ python manage.py runserver
```

Log into the Django admin with your superuser account at:

[http://localhost:8000/admin/](http://localhost:8000/admin/)

Browse the REST API at:

[http://localhost:8000/api/v1/](http://localhost:8000/api/v1/).


For Create or Update playlist
### Request Params:-

```
media type application/json
{
       
            "name": "playlist210",
            "tracks": ["aeae58d5-5180-4aef-ba80-1c75cf28cd4a","9783f3c6-8d09-4d6d-aa2c-d6ed43785240"]
}
```
