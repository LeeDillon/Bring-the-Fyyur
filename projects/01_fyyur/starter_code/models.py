from flask_sqlalchemy import SQLAlchemy

# Initialized without explicit app (Flask instance)
db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    address = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.String(120), nullable=False, default=False)
    seeking_description = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    shows = db.relationship('Show', backref='venue', lazy='joined', cascade="all, delete")
    
    # def __repr__(self):
    #     return f"<Venue id={self.id} name={self.name} city={self.city} state={self.state} address={self.address} phone={self.phone} self={self.genres} self={self.image_link} self={self.facebook_link} self={self.website} self={self.seeking_talent} self={self.seeking_description}>"
    
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.String(120), nullable=False, default=False)
    seeking_description = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    shows = db.relationship('Show', backref='artist', lazy='joined', cascade="all, delete")

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):
    __tablename__ = 'shows'

    # id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), primary_key=True)
    start_time = db.Column(db.DateTime, primary_key=True)