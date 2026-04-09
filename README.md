# MaddestLibber

Make some improvosational stories!

## Running

- Set up a Python virtual environment

  ```bash
  python -m venv venv
  venv\scripts\activate
  ```

- Install project dependencies

  ```bash
  pip install -r requirements.txt
  ```

- Create your `.env` file

  ```bash
  cp .env.example .env
  ```

- Run the app

  ```bash
  flask run --debug
  ```

## Developing Your Own Version

To develop your own version of this project, you can `clone` or `fork` this repo.

- `git clone <repo url>` makes a copy of the repo, but still considers the upstream (parent) repo to be this repo. This is fine for development and testing, but the remote repo still belongs to me.
- Forking the repo makes a copy of the repo on _your_ GitHub account, meaning that you have full control of it from that point forward. This is the better approach when you want to make your own version of an existing project, as opposed to contributing to the original one.

## Database Migrations

### Making New Migrations

`flask db migrate -m "commit message"`

### Applying Migrations to Existing DBs

`flask db upgrade`

## Celery Worker

A celery worker is set up and configured for running asynchronous tasks. This will be used in the future for email registration, etc., but for now is not used.

To stand up the celery worker:

- Configure a Redis instance (Docker container on local machine with port 6374 is used here)
- Install redis and celery via pip `pip install redis celery`
- Launch the celery worker `celery -A celery_worker.celery worker --pool=solo --loglevel=info`

## Credits

- [Flask](https://flask.palletsprojects.com/en/stable/)
