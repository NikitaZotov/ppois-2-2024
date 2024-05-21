# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Models
class Studio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # Связь один ко многим с площадками
    platforms = db.relationship('Platform', secondary='studio_platform', backref='studio')

studio_platform = db.Table('studio_platform',
    db.Column('studio_id', db.Integer, db.ForeignKey('studio.id'), primary_key=True),
    db.Column('platform_id', db.Integer, db.ForeignKey('platform.id'), primary_key=True)
)

class Platform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform_name = db.Column(db.String(100), nullable=False)
    studio_id = db.Column(db.Integer, db.ForeignKey('studio.id'), nullable=True)

    # Связь многие ко многи с сценариями через доп таблицу platfrom_script
    scripts = db.relationship('Script', secondary='platform_script', backref='platform')

    # Связь многие ко многи с актерами через доп таблицу platfrom_actor
    actors = db.relationship('Actor', secondary='platform_actor', backref='platform')

    # Связь многие ко многи с режиссерами через доп таблицу platfrom_director
    directors = db.relationship('Director', secondary='platform_director', backref='platform')

platform_script = db.Table('platform_script',
    db.Column('platform_id', db.Integer, db.ForeignKey('platform.id'), primary_key=True),
    db.Column('script_id', db.Integer, db.ForeignKey('script.id'), primary_key=True)
)

platform_actor = db.Table('platform_actor',
    db.Column('platform_id', db.Integer, db.ForeignKey('platform.id'), primary_key=True),
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'), primary_key=True)
)

platform_director = db.Table('platform_director',
    db.Column('platform_id', db.Integer, db.ForeignKey('platform.id'), primary_key=True),
    db.Column('director_id', db.Integer, db.ForeignKey('director.id'), primary_key=True)
)

class Script(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False) 

class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Director(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
