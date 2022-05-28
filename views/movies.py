# - [ ]  GET /movies — получить все фильмы.
# - [ ]  GET /movies/3 — получить фильм по ID.
# - [ ]  GET /movies?director_id=15 — получить все фильмы режиссера.
# - [ ]  GET /movies?genre_id=3 — получить все фильмы жанра.
# - [ ]  GET /movies?year=2007 — получить все фильмы за год.

# - [ ]  POST /movies — создать фильм.

# - [ ]  PUT /movies/1 — изменить информацию о фильме.

# - [ ]  DELETE /movies — удалить фильм.

from flask_restx import Resource, Namespace
from models import Movie, Director, Genre, MovieSchema, DirectorSchema, GenreSchema
from setup_db import db
from flask import request

movies_ns = Namespace('movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movies_ns.route('/')
class MovieView(Resource):
    def get(self):
        genre_id = request.args.get('genre_id')
        director_id = request.args.get('director_id')
        year = request.args.get('year')

        if genre_id and genre_id != '':
            select = db.session.query(Movie.title)
            filter = select.filter(Movie.genre_id == genre_id).all()
            if not filter:
                return f"movie genre_id={genre_id} not found", 404
            return movies_schema.dump(filter), 200

        elif director_id and director_id != '':
            select = db.session.query(Movie.title)
            filter = select.filter(Movie.director_id == director_id).all()
            if not filter:
                return f"movie director_id={director_id} not found", 404
            return movies_schema.dump(filter), 200

        elif year and year != '':
            select = db.session.query(Movie.title)
            filter = select.filter(Movie.year == year).all()
            if not filter:
                return f"movie year={year} not found", 404
            return movies_schema.dump(filter), 200

        select = db.session.query(Movie.id, Movie.title).all()
        return movies_schema.dump(select), 200

    def post(self):
        data = request.get_json()
        new_movie = Movie(**data)
        with db.session.begin():
            db.session.add(new_movie)
        return "", 204



@movies_ns.route('/<int:mid>')
class ReviewView(Resource):
    def get(self, mid):
        select = db.session.query(Movie.id,
                                  Movie.title,
                                  Movie.description,
                                  Movie.trailer,
                                  Movie.year,
                                  Movie.rating,
                                  Genre.name.label('genre_name'),
                                  Director.name.label('director_name'))
        join1 = select.join(Genre, Movie.genre_id == Genre.id)
        join2 = join1.join(Director, Movie.director_id == Director.id)
        where = join2.filter(Movie.id == mid).one()
        return movie_schema.dump(where), 200

    def put(self, mid):
        data = request.get_json()
        movie = Movie.query.get(mid)
        if data['title']:
            movie.title = data['title']
        if data['description']:
            movie.description = data['description']
        if data['trailer']:
            movie.trailer = data['trailer']
        if data['year']:
            movie.year = data['year']
        if data['rating']:
            movie.rating = data['rating']
        if data['genre_id']:
            movie.genre_id = data['genre_id']
        if data['director_id']:
            movie.director_id = data['director_id']
        db.session.add(movie)
        db.session.commit()
        return "", 204

    def delete(self, mid):
        movie = Movie.query.get(mid)
        db.session.delete(movie)
        db.session.commit()
        return "", 204