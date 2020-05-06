#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import render_template, request, Response, flash, redirect, url_for, jsonify
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import ArtistForm, VenueForm, ShowForm
from models import *
from config import *

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
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  return render_template('pages/venues.html', areas=City.query.all());

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form['search_term']
  query = Venue.query.filter(Venue.name.ilike('%{}%'.format(search_term)))
  response = {
    "count": query.count(),
    "data": query.all()
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', search_term))
  
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  #TODO: Original version passed city and state in a different way...
  return render_template('pages/show_venue.html', venue=Venue.query.get(venue_id))

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  return render_template('pages/artists.html', artists=Artist.query.all())

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form['search_term']
  query = Artist.query.filter(Artist.name.ilike('%{}%'.format(search_term)))
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

@app.route('/artists/create', methods=['GET'])
def create_artist():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  data = request.get_json()
  success = 'true'
  message = ''
  try:
    artist = Artist()
    artist.name = data['name']
    artist.phone = data['phone']
    artist.image_link = data['image']
    artist.facebook_link = data['facebook']
    artist.website = data['website']
    artist.seeking_venue = data['isSeeking']
    artist.seeking_description = data['seekingDesc']
    # TODO: Add genres
    # TODO: Deal with city info
    cityID = 0
    city_query = City.query.filter(City.state==data['state']).filter(City.city==data['city']).all()
    if(len(city_query) > 0):
      cityID = city_query[0].id
    else:
      newCity = City()
      newCity.city = data['city']
      newCity.state = data['state']
      db.session.add(newCity)
      db.session.commit()
      cityID = newCity.id
    artist.city_id = cityID
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + data['name'] + ' was successfully listed!')
  except Exception as e:
    print(e)
    db.session.rollback()
    success = 'false'
    message = 'Something went wrong...'
  finally:
    db.session.close()
  print(data)
  return jsonify({
    'redirect': '/artists',
    'success': success,
    'error': message
    })
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  return render_template('pages/shows.html', shows=Show.query.all())

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

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
