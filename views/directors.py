
# - [ ]  GET /directors — получить всех режиссеров.
# - [ ]  GET /directors/3 — получить режиссера по ID.

from flask_restx import Resource, Namespace
from models import Movie, Director, Genre, MovieSchema, DirectorSchema, GenreSchema
from setup_db import db
from flask import request

directors_ns = Namespace('directors')

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@directors_ns.route('/')
class DirectorView(Resource):
    def get(self):
        select = db.session.query(Director.name).all()
        return directors_schema.dump(select), 200


@directors_ns.route('/<int:did>')
class DirectorView(Resource):
    def get(self, did):
        select = db.session.query(Director.id,
                                  Director.name)
        where = select.filter(Director.id == did).one()
        return director_schema.dump(where), 200
