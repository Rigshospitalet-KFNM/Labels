![Rigshospitalets logo](config/core/static/core/graphics/Logo_Rigshospitalet.png)

# Labels

This repository serves to provide an improved solution to printing standardized labels for the chemisty department. This program looks to replace the currently used [solution](http://hopper.petnet.rh.dk/labels/). 

## Focus

The repository should prioritize; facilitated code handovers, ease of use for the end user, and easy database management, both for users and developers.


## how to run locally

>To run on a linux distribution it's recommended to use a virtual environment.

<br />

Download the appropriate dependencies according to use case:
```
 pip install -r requirements/base.txt
```
(Optional – for local development, testing, linting, etc.):
```
 pip install -r requirements/dev.txt
```
<br />
Ensure nescesary environment variables in a .env file, expected variables can be found in .env.dist.

<br />
Apply database migrations, to initalize schema:

```
python manage.py migrate
```
<br />
Load the predefined protected components:

```
python manage.py loaddata components.json
```

<br />
Run the development server:

```
python manage.py runserver
```