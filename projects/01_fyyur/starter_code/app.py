#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify, abort, session
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import datetime
import sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.String(), nullable=False)
    address = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.String(120), nullable=False, default=False)
    seeking_description = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    shows = db.relationship('Show', backref='Venue', lazy=True)

    # def past_shows(self):
    #   return Show.get_past_by_venue(self.id)


    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.String(120), nullable=False, default=False)
    seeking_description = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    shows = db.relationship('Show', backref='Artist', lazy=True)

    # def upcoming_shows_count(self):
    #   return self.query.join(Show).filter_by(artist_id=self.id).filter(
    #   Show.start_time > datetime.now()).count()

    # def past_shows_count(self):
    #   return self.query.join(Show).filter_by(artist_id=self.id).filter(
    #   Show.start_time < datetime.now()).count()

    # def past_shows(self):
    #   return Show.get_past_by_artist(self.id)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):
    __tablename__ = 'shows'

    # id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), primary_key=True)
    start_time = db.Column(db.DateTime(timezone=True))

    # def __repr__(self):
    #   return '<Show {} {}>'.format(self.artist_id, self.venue_id)

    # @classmethod
    # def get_past_by_venue(cls, venue_id):    
    #   shows = cls.query.filter_by(venue_id=venue_id).filter(cls.start_time < datetime.now()).all()
    #   return [show.show_details for show in shows]

    # @classmethod
    # def get_past_by_artist(cls, artist_id):
    #   shows = cls.query.filter_by(artist_id=artist_id).filter(cls.start_time < datetime.now()).all()
    #   return [show.show_details for show in shows]

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  # date = dateutil.parser.parse(value)
  if isinstance(value, str):
      date = dateutil.parser.parse(value)
  else:
      date = value
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

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
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  data = []
  listOfAllVenues = Venue.query.all()
  for area in listOfAllVenues:
    area={
      "city": area.city,
      "state": area.state,
      "venues": [{
        "id": area.id,
        "name": area.name
      }]
      }
    data.append(area)
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term', '')
  venues = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
  response={
    "count": len(venues),
    "data": []
  }
  for venue in venues:
    response["data"].append({
      "id": venue.id,
      "name": venue.name
    }) 
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)
  pastShowsInfo = Show.query.filter(Show.venue_id==venue_id).filter(Show.start_time < datetime.datetime.now()).all()
  upcomingShowsInfo = Show.query.filter(Show.venue_id==venue_id).filter(Show.start_time > datetime.datetime.now()).all()
  past_shows = []
  for show in pastShowsInfo:    
    artist = Artist.query.get(show.artist_id)
    past_shows.append({
      "artist_id": artist.id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": show.start_time
    })
  upcoming_shows = []
  for show in upcomingShowsInfo:    
    artist = Artist.query.get(show.artist_id)
    upcoming_shows.append({
      "artist_id": artist.id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": show.start_time
    })
  data = {
      "id": venue.id,
      "name": venue.name,
      "genres": venue.genres,
      "city": venue.city,
      "state": venue.state,
      "phone": venue.phone,
      "seeking_venue": True if venue.seeking_talent in ('y', True) else False,
      "seeking_description": venue.seeking_description,
      "image_link": venue.image_link,
      "facebook_link": venue.facebook_link,
      "website_link": venue.website,
      "past_shows": past_shows,
      "upcoming_shows": upcoming_shows,
  }
  return render_template('pages/show_venue.html', venue=data)  

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  error = False
  try:
    name = request.form['name']
    genres = request.form['genres']
    address = request.form['address']
    city = request.form['city']
    state = request.form['state']
    phone = request.form['phone']
    website = request.form['website_link']
    facebook_link = request.form['facebook_link']
    seeking_talent = request.form['seeking_talent']
    seeking_description = request.form['seeking_description']
    image_link = request.form['image_link']
    venue = Venue(name=name,genres=genres,address=address,city=city,state=state,phone=phone,website=website,facebook_link=facebook_link,seeking_talent=seeking_talent,seeking_description=seeking_description,image_link=image_link)
    db.session.add(venue)
    db.session.commit()
  except:
    db.session.rollback()
    error = True
    print(sys.exc_info)
  finally:
    db.session.close()
  if error:
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    abort(500)
  else:
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
    return render_template('pages/home.html')
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  # flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  # return render_template('pages/home.html')

@app.route('/venues/<venue_id>/delete', methods=['DELETE'])
def delete_venue(venue_id):
  error = False
  try:
    thisVenue = Venue.query.get(venue_id)
    db.session.delete(thisVenue)
    db.session.commit()
  except:
    db.session.rollback()
    error = True
    print(sys.exc_info)
  finally:
    db.session.close()
  if error:
    flash('An error occurred. Venue could not be deleted.')
    abort(500)
  else:
    flash('Venue was successfully deleted!')
    return None
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term', '')
  artists = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
  response={
    "count": len(artists),
    "data": []
  }
  for artist in artists:
    response["data"].append({
      "id": artist.id,
      "name": artist.name
    }) 
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  artistInfo = Artist.query.get(artist_id)
  pastShowsInfo = Show.query.filter(Show.artist_id==artist_id).filter(Show.start_time < datetime.datetime.now()).all()
  upcomingShowsInfo = Show.query.filter(Show.artist_id==artist_id).filter(Show.start_time > datetime.datetime.now()).all()

  past_shows = []
  for show in pastShowsInfo:    
    venue = Venue.query.get(show.venue_id)
    past_shows.append({
      "venue_id": venue.id,
      "venue_name": venue.name,
      "venue_image_link": venue.image_link,
      "start_time": show.start_time
    })
  upcoming_shows = []
  for show in upcomingShowsInfo:    
    venue = Venue.query.get(show.venue_id)
    upcoming_shows.append({
      "venue_id": venue.id,
      "venue_name": venue.name,
      "venue_image_link": venue.image_link,
      "start_time": show.start_time
    })
  data = {
      "id": artistInfo.id,
      "name": artistInfo.name,
      "genres": artistInfo.genres,
      "city": artistInfo.city,
      "state": artistInfo.state,
      "phone": artistInfo.phone,
      "seeking_venue": True if artistInfo.seeking_venue in ('y', True) else False,
      "seeking_description": artistInfo.seeking_description,
      "image_link": artistInfo.image_link,
      "facebook_link": artistInfo.facebook_link,
      "website_link": artistInfo.website,
      "past_shows": past_shows,
      "upcoming_shows": upcoming_shows,
  }
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  error = False
  try:
    name = request.form['name']
    genres = request.form['genres']
    city = request.form['city']
    state = request.form['state']
    phone = request.form['phone']
    website = request.form['website_link']
    facebook_link = request.form['facebook_link']
    seeking_venue = request.form['seeking_venue']
    seeking_description = request.form['seeking_description']
    image_link = request.form['image_link']
    artist = Artist(name=name,genres=genres,city=city,state=state,phone=phone,website=website,facebook_link=facebook_link,seeking_venue=seeking_venue,seeking_description=seeking_description,image_link=image_link)
    db.session.add(artist)
    db.session.commit()
  except:
    db.session.rollback()
    error = True
    print(sys.exc_info)
  finally:
    db.session.close()
  if error:
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    abort(500)
  else:
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
    return render_template('pages/home.html')
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')



#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  showsInfo = db.session.query(Show).join(Artist).join(Venue).all()
  data = []
  for show in showsInfo:
    data.append({
      "venue_id": show.venue_id,
      "venue_name": show.Venue.name,
      "artist_id": show.artist_id,
      "artist_name": show.Artist.name, 
      "artist_image_link": show.Artist.image_link,
      "start_time": show.start_time
    })
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  error = False
  try:
    artist_id = request.form['artist_id']
    venue_id = request.form['venue_id']
    start_time = request.form['start_time']
    show = Show(artist_id=artist_id,venue_id=venue_id,start_time=start_time)
    db.session.add(show)
    db.session.commit()
  except:
    db.session.rollback()
    error = True
    print(sys.exc_info)
  finally:
    db.session.close()
  if error:
    flash('An error occurred. Show could not be listed.')
    abort(500)
  else:
    flash('Show was successfully listed!')
    return render_template('pages/home.html')
  # on successful db insert, flash success
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  # return render_template('pages/home.html')

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
