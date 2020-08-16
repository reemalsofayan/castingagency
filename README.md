################ casting-agency ##########################

The same proposed  udacity capstone project.


application live at[ https://castingagency-deploy.herokuapp.com/]

## Technologies

- [Python3](https://www.python.org/download/releases/3.0/)
- [Flask](https://palletsprojects.com/p/flask/)
- [Postgres](https://www.postgresql.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
- [psycopg2](http://initd.org/psycopg/)
- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/#)
- [alembic](https://alembic.sqlalchemy.org/en/latest/)

## Dependencies

install the requiremnets file using 
pip install -r requirements.txt


## Motivation

this is the final project of FSND in order to graduate



## API Authentication: 

you can log in to the API using the link:

https://fsnd-castingagency.au.auth0.com/authorize?
 audience=Casting&
 response_type=token&
 client_id=7b4nVmc85DgE0ZSkw2zytQHHxjA23OMd&
 redirect_uri=https://castingagency-deploy.herokuapp.com/

using the following users :

-EXECUTIVE_PRODUCER

USERNAME: executive_producer@casting.com
PASSWORD: executive_producer123


-CASTING_DIRECTOR 

USERNAME: casting_director@casting.com
PASSWORD: casting_director123


-CASTING_ASSISTANT

USERNAME: casting_assistant@casting.com
PASSWORD: casting_assistant123




## How to run the app

go the the project directory and run

export FLASK_APP=app
export FLASK_DEBUG=True
flask run
```


## Unit tests

go the the project directory and run

python test.py



##endpoints

 the endpoints are tested using postman tool

### GET http://127.0.0.1:5000/movies

Response:

{
  "movies": [
    {
      "id": 132,
      "release_date": 2017,
      "title": "The Accountant"
    }
  ],
  "success": true
}

//---------------------------------------------------
### POST http://127.0.0.1:5000/movies

DATA:

 {
         "title":"The Accountant",
         "release_date":2017
        

      }

Response:

{
  "movie": {
    "id": 132,
    "release_date": 2017,
    "title": "The Accountant"
  },
  "success": true
}

//------------------------------------------------------

### PATCH http://127.0.0.1:5000/movies/132

DATA:
 {
         "title":"The Accountant",
         "release_date":2016
        

            }

Response:

{
  "movie": {
    "id": 132,
    "release_date": 2016,
    "title": "The Accountant"
  },
  "success": true
}

//---------------------------------



### DELETE http://127.0.0.1:5000/movies/132


Response:


{
  "delete": 132,
  "success": true
}

//-------------------------------

### GET http://127.0.0.1:5000/actors



Response:

{
  "actors": [
    {
      "age": 48,
      "gender": "male",
      "id": 67,
      "name": "richard Armitage"
    }
  ],
  "success": true
}
```
//-------------------------------------------------
### POST http://127.0.0.1:5000/actors


Data:

{
  "name": "richard Armitage",
  "age":48,
  "gender": "male"

}

Response:

{
  "actor": {
    "age": 48,
    "gender": "male",
    "id": 67,
    "name": "richard Armitage"
  },
  "success": true
}

//---------------------------------
### PATCH http://127.0.0.1:5000/actors/67

Edit data on a actor in the db.

Data:

{
  "name": "james Armitage",
  "age":48,
  "gender": "male"

}


Response:

{
  "actor": {
    "age": 48,
    "gender": "male",
    "id": 67,
    "name": "james Armitage"
  },
  "success": true
}
//-----------------------------------------

### DELETE http://127.0.0.1:5000/actors/67


Response:

{
  "delete": 67,
  "success": true
}