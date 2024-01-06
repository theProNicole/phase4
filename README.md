# The Gym :muscle:
## Phase 4 Full-Stack Application Project
Creators: Charles Featherstone, Nicole Casteel, & Emily Valdez

## Introduction
Welcome to The Gym! If you are a new user, feel free to have a look around at your leisure. We offer several gym locations, as well as (non-paid) client reviews. Once you register with us and select your overall goals, the Workout Schedule will populate with exercises custom to you. If you have any questions, please visit our FAQ, or reach out to us at (555) 555-5555.

## Setup

### `server/`

The `server/` directory contains all of our backend code.

`app.py` is the Flask application. To download the dependencies for the backend server, run:

```console
pipenv install
pipenv shell
```

You can run the Flask API on [`localhost:5555`](http://localhost:5555) by
running:

```console
python server/app.py
```


### `client/`

The `client/` directory contains all of our frontend code. 

To download the dependencies for the frontend client, run:

```console
npm install --prefix client
```

Start up our React app on [`localhost:3000`](http://localhost:3000) by
running:

```sh
npm start --prefix client
```

## Seeding The Database

Change into the `server` directory:

```console
cd server
```

Seed the database by running:
```
python seed.py
```
---

## Models
Our gym landing page showcases three main models: Reviews, Locations, and Workout Schedule.

