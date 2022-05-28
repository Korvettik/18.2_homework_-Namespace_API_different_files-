# - [ ]  GET /genres — получить все жанры.
# - [ ]  GET /genres/3 — получить жанр по ID.


from flask_restx import Resource, Namespace
from models import Movie, Director, Genre, MovieSchema, DirectorSchema, GenreSchema
from setup_db import db
from flask import request

genre_ns = Namespace('genres')

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@genre_ns.route('/')
class GenreView(Resource):
    def get(self):
        select = db.session.query(Genre.name).all()
        return genres_schema.dump(select), 200


@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    def get(self, gid):
        select = db.session.query(Genre.id,
                                  Genre.name)
        where = select.filter(Genre.id == gid).one()
        return genre_schema.dump(where), 200