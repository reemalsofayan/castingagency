# from flask import Flask, render_template, request, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# import os
from sqlalchemy import Column, String, Integer, create_engine,Table,ForeignKey
# from flask_sqlalchemy import SQLAlchemy
# import json
from app import db

# db = SQLAlchemy()
# database_path = 'postgresql://postgres:root@localhost:5432/castingagency'

# def setup_db(app, database_path):
#     app.config["SQLALCHEMY_DATABASE_URI"] = database_path
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#     db.app = app
#     db.init_app(app)


class Movie(db.Model):

    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String(80), unique=True, nullable=False)
    release_date = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Movie {self.id} {self.title}>"

    def insert(self):
  
        db.session.add(self)
        db.session.commit()

    def delete(self):
 
        db.session.delete(self)
        db.session.commit()

   
    def update(self):
    
        db.session.commit()

    def format(self):
        
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
        }


class Actor(db.Model):
  
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(6), nullable=False)
    
    
                             

    def __repr__(self):
        return f"<Actor {self.id} {self.name}>"

    def insert(self):
     
        db.session.add(self)
        db.session.commit()

    def delete(self):
   
        db.session.delete(self)
        db.session.commit()

    
    def update(self):
  
        db.session.commit()

    def format(self):
       
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            
        }