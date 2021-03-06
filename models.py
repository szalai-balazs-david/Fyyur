
from sqlalchemy_utils import aggregated
from extensions import db
import datetime

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

venue_genres = db.Table('venue_genres',
    db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'), primary_key=True)
)

artist_genres = db.Table('artist_genres',
    db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'), primary_key=True)
)

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    city_id = db.Column(db.Integer, db.ForeignKey('City.id'), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    website = db.Column(db.String(120), nullable=True)
    seeking_talent = db.Column(db.Boolean, nullable=True)
    seeking_description = db.Column(db.String, nullable=True)
    genres = db.relationship('Genre', secondary=venue_genres,
      backref=db.backref('venues', lazy=True))
    regitration_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    @aggregated('upcoming_shows', db.Column(db.Integer))
    def num_upcoming_shows(self):
        return db.func.count(Show.id)
    upcoming_shows = db.relationship('Show', 
      primaryjoin='and_(Venue.id == Show.venue_id, cast(Show.start_time, Date) >= func.current_date())',
      order_by='Show.start_time')
    @aggregated('past_shows', db.Column(db.Integer))
    def num_past_shows(self):
        return db.func.count(Show.id)
    past_shows = db.relationship('Show', 
      primaryjoin='and_(Venue.id == Show.venue_id, cast(Show.start_time, Date) < func.current_date())',
      order_by='Show.start_time')
    shows = db.relationship('Show', cascade="delete", backref=db.backref('venue', lazy=True))

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    city_id = db.Column(db.Integer, db.ForeignKey('City.id'), nullable=False)
    phone = db.Column(db.String(120), nullable=True)
    image_link = db.Column(db.String(500), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    website = db.Column(db.String(120), nullable=True)
    seeking_venue = db.Column(db.Boolean, nullable=True)
    seeking_description = db.Column(db.String, nullable=True)
    genres = db.relationship('Genre', secondary=artist_genres,
      backref=db.backref('artists', lazy=True))
    regitration_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    @aggregated('upcoming_shows', db.Column(db.Integer))
    def num_upcoming_shows(self):
        return db.func.count(Show.id)
    upcoming_shows = db.relationship('Show', 
      primaryjoin='and_(Artist.id == Show.artist_id, cast(Show.start_time, Date) >= func.current_date())',
      order_by='Show.start_time')
    @aggregated('past_shows', db.Column(db.Integer))
    def num_past_shows(self):
        return db.func.count(Show.id)
    past_shows = db.relationship('Show', 
      primaryjoin='and_(Artist.id == Show.artist_id, cast(Show.start_time, Date) < func.current_date())',
      order_by='Show.start_time')
    shows = db.relationship('Show', cascade="delete", backref=db.backref('artist', lazy=True))

class City(db.Model):
    __tablename__ = 'City'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    venues = db.relationship('Venue', backref='city', lazy=True)
    artists = db.relationship('Artist', backref='city', lazy=True)

    def __repr__(self):
        return f'{self.city}, {self.state}'

class Genre(db.Model):
    __tablename__ = 'Genre'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)

    def __repr__(self):
        return f'{self.name}'

class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime(), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
