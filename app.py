import sys
import json
import dateutil.parser
import babel
from sqlalchemy import func
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from config import Config
from flask import jsonify
from auth import AuthError, requires_auth
import os



app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import *

# a welcoming endpoint to the application
@app.route('/')
def index():

    return jsonify({
        'message': 'Welcome to Casting Agency , you may start to explore the endpoints',
        'success': True
    })

# this endpint will alow the user to add new movie
@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def add_movie(payload):
    # get the body request
    body = request.get_json()
    title=body.get('title',None)
    release_date=body.get('release_date',None)
    
    
    if  title is None or release_date is None :
        abort(422)
    try:

        new_movie = Movie(title=title,release_date=release_date)
        new_movie.insert()
            
        
        return jsonify({
            'movie': new_movie.format(),
            'success': True
        })

    except BaseException:
        abort(422)

# this endpint will alow the user to retrieve all movies
@app.route('/movies')
@requires_auth('get:movies')
def get_movies(payload):
    
    # try:
        movies = Movie.query.all()
        movies = [movie.format() for movie in movies]
        return jsonify({
            'success': True,
            'movies': movies
        })
    # except:
    #     abort(422)
# this endpint will alow the user to modify an existing movie
@app.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movies')
def modify_movie(payload, movie_id):
    body = request.get_json()
    title = body.get('title',None)
    release_date = body.get('release_date',None)

    try:
        # check if the movie exist in the database
        movie = Movie.query.filter_by(id=movie_id).one_or_none()
        if movie is None:
            abort(404)

        if release_date is not None:
            movie.release_date = release_date
        else:
            abort(400)      

        if title is not None:
            movie.title = title 
        else:
            abort(400)  


        movie.update()  

        return jsonify({
            'success': True,
            'movie': movie.format()
        })

    except:   
        abort(422)


# this endpint will alow the user delete a movie
@app.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(payload, movie_id):
    movie = Movie.query.filter_by(id=movie_id).one_or_none()

    if  movie is None:
        abort(404)

    try:
        movie.delete()
        return jsonify({
            'success': True,
            'delete': movie_id
            })
    except:
        abort(422)

# this endpint will alow the user to add an actor to database
@app.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def add_actor(payload):
    
    body = request.get_json()
    name = body.get('name',None)
    age = body.get('age',None)
    gender = body.get('gender',None)
    
    
    if name is None:
        abort(422)

    if age is None:
        abort(422) 

    if gender is None:
        abort(422)       

    
    try:
        new_actor = Actor(name=name,age=age,gender=gender)
        new_actor.insert()
            
        
        return jsonify({
            'actor': new_actor.format(),
            'success': True
        })
    except:
        abort(422)


# this endpint will alow the user to retrieve all actors from database
@app.route('/actors')
@requires_auth('get:actors')
def get_actors(payload):
    
    try:
        actors = Actor.query.all()
        actors = [actor.format() for actor in actors]
        

        return jsonify({
            'actors':actors,
            'success': True
        })
    except:
        abort(422)

# this endpint will alow the user to modify an existing actor
@app.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('patch:actors')
def modify_actor(payload, actor_id):
    body = request.get_json()

    name = body.get('name',None)
    age = body.get('age',None)
    gender = body.get('gender',None)

    try:
        # check if actor exist in database
        actor = Actor.query.filter_by(id=actor_id).one_or_none()
        if actor is None:
            abort(404)

        if name is not None:
            actor.name  = name  
        else:
            abort(400)
        

        if age is not None:
            actor.age = age
        else:
            abort(400)    

        if gender is not None:
            actor.gender  = gender   
        else:
            abort(400)        



        actor.update()  

        return jsonify({
            'success': True,
            'actor': actor.format()
        })

    except:   
        abort(422)


# this endpint will alow the user to delete an actor
@app.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(payload, actor_id):
    actor = Actor.query.filter_by(id=actor_id).one_or_none()

    if  actor is None:
        abort(404)

    try:
        actor.delete()
        return jsonify({
            'success': True,
            'delete': actor_id
            })

    except:
        abort(422)


    # return app



@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422





@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error
    }), error.status_code

