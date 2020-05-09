#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from models import Artist, Venue, Genre, City, Show
from forms import ArtistForm, VenueForm, ShowForm
from extensions import csrf, moment, db, migrate
from sqlalchemy import or_, and_

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

def register_extensions(app):
  csrf.init_app(app)
  db.init_app(app)
  migrate.init_app(app, db)
  moment.init_app(app)

app = Flask(__name__)
app.config.from_object('config')
register_extensions(app)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  #date = dateutil.parser.parse(value)
  date = value
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Custom stuff.
#----------------------------------------------------------------------------#

def get_city_id(city, state):
  cityID = 0
  city_query = City.query.filter(City.state==state).filter(City.city==city).all()
  if(len(city_query) > 0):
    cityID = city_query[0].id
  else:
    newCity = City()
    newCity.city = city
    newCity.state = state
    db.session.add(newCity)
    db.session.commit()
    cityID = newCity.id
  return cityID

def search_for_city(search_term, city):
  if ', ' not in search_term:
    return False
  city_name = search_term.split(', ')[0]
  state_name = search_term.split(', ')[1]
  return and_(
    city.city.ilike('%{}%'.format(city_name)),
    city.state.ilike('%{}%'.format(state_name)))

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  venue_query = Venue.query.limit(10)
  artist_query = Artist.query.limit(10)
  venues = {
    'count': venue_query.count(),
    'list': venue_query.all()
  }
  artists = {
    'count': artist_query.count(),
    'list': artist_query.all()
  }
  return render_template('pages/home.html', venues=venues, artists=artists)


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  return render_template('pages/venues.html', areas=City.query.filter(City.venues.any()).all())

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form['search_term']
  query = Venue.query.join(Venue.city).filter(
    or_(
      Venue.name.ilike('%{}%'.format(search_term)),
      search_for_city(search_term, City)))
  response = {
    "count": query.count(),
    "data": query.all()
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', search_term))
  
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  return render_template('pages/show_venue.html', venue=Venue.query.get(venue_id))

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET', 'POST'])
def create_venue_submission():
  form = VenueForm()
  if form.validate_on_submit():
    try:
      venue = Venue()
      venue.name = form.name.data
      venue.city_id = get_city_id(form.city.data, form.state.data)
      venue.address = form.address.data
      venue.facebook_link = form.facebook.data
      venue.image_link = form.image.data
      venue.phone = form.phone.data
      venue.seeking_talent = form.isSeeking.data
      venue.seeking_description = form.seekingDescription.data
      venue.genres = form.genres.data
      db.session.add(venue)
      db.session.commit()
      flash('Venue ' + venue.name + ' was successfully listed!')
    except Exception as e:
      flash('An error occurred: ' + str(e))
      db.session.rollback()
    finally:
      db.session.close()
    return redirect(url_for('venues'))
  return render_template('forms/new_venue.html', form=form)

@csrf.exempt
@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue_v2(venue_id):
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
  except Exception as e:
    print(e)
    db.session.rollback()
  finally:
    db.session.close()
  return jsonify({
    'redirect': '/venues'
  })

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  return render_template('pages/artists.html', artists=Artist.query.order_by('name').all())

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form['search_term']
  query = Artist.query.join(Artist.city).filter(
    or_(
      Artist.name.ilike('%{}%'.format(search_term)),
      search_for_city(search_term, City)))
  response = {
    "count": query.count(),
    "data": query.all()
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', search_term))
  
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  return render_template('pages/show_artist.html', artist=Artist.query.get(artist_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET', 'POST'])
def create_artist_submission():
  form = ArtistForm()
  if form.validate_on_submit():
    try:
      artist = Artist()
      artist.name = form.name.data
      artist.city_id = get_city_id(form.city.data, form.state.data)
      artist.phone = form.phone.data
      artist.image_link = form.image.data
      artist.facebook_link = form.facebook.data
      artist.website = form.website.data
      artist.seeking_venue = form.isSeeking.data
      artist.seeking_description = form.seekingDesc.data
      artist.genres = form.genres.data
      db.session.add(artist)
      db.session.commit()
      flash('Artist ' + artist.name + ' was successfully listed!')
    except Exception as e:
      flash('An error occurred: ' + str(e))
      db.session.rollback()
    finally:
      db.session.close()
    return redirect(url_for('artists'))
  return render_template('forms/new_artist.html', form=form)

@csrf.exempt
@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist_v2(artist_id):
  try:
    artist = Artist.query.get(artist_id)
    db.session.delete(artist)
    db.session.commit()
  except Exception as e:
    print(e)
    db.session.rollback()
  finally:
    db.session.close()
  return jsonify({
    'redirect': '/artists'
  })

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  return render_template('pages/shows.html', shows=Show.query.all())

@app.route('/shows/create', methods=['GET', 'POST'])
def create_show_submission():
  form = ShowForm()
  if form.validate_on_submit():
    try:
      show = Show()
      show.artist_id = form.artist_id.data.id
      show.venue_id = form.venue_id.data.id
      show.start_time = form.start_time.data
      db.session.add(show)
      db.session.commit()
      flash('Show was successfully listed!')
    except Exception as e:
      flash('An error occurred: ' + str(e))
      db.session.rollback()
    finally:
      db.session.close()
    return redirect(url_for('shows'))
  return render_template('forms/new_show.html', form=form)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
