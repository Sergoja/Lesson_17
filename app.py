# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")

class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()


# class DirectorSchema(Schema):
#     id = fields.Int()
#     name = fields.Str()
#
#
# class GenreSchema(Schema):
#     id = fields.Int()
#     name = fields.Str()


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

# director_schema = DirectorSchema()
# directors_schema = DirectorSchema(many=True)
#
# genre_schema = GenreSchema()
# genres_schema = GenreSchema(many=True)

api = Api(app)
movie_ns = api.namespace('movies')
# director_ns = api.namespace('directors')
# genre_ns = api.namespace('genres')


@movie_ns.route('/')
class MovieView(Resource):
    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        if director_id is not None:
            all_movies = db.session.query(Movie).filter(Movie.director_id == director_id).all()
            return movies_schema.dump(all_movies), 200
        elif genre_id is not None:
            all_movies = db.session.query(Movie).filter(Movie.genre_id == genre_id).all()
            return movies_schema.dump(all_movies), 200
        else:
            all_movies = db.session.query(Movie).all()
            return movies_schema.dump(all_movies), 200


@movie_ns.route('/<int:uid>')
class MovieView(Resource):
    def get(self, uid: int):
        try:
            movie = db.session.query(Movie).filter(Movie.id == uid).one()
            return movie_schema.dump(movie), 200
        except Exception:
            return "Not found", 404


if __name__ == '__main__':
    app.run(debug=True)
