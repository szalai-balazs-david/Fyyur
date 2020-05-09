from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, TextField, SubmitField, FileField, BooleanField, IntegerField
from wtforms.validators import DataRequired, AnyOf, URL, ValidationError, Regexp, Length, Email, Optional
from models import Genre, Venue, Artist
import phonenumbers

def validate_phone(form, field):
    if len(field.data) > 16:
        raise ValidationError('Invalid phone number.')
    try:
        input_number = phonenumbers.parse(field.data)
        if not (phonenumbers.is_valid_number(input_number)):
            raise ValidationError('Invalid phone number.')
    except:
        try:
            input_number = phonenumbers.parse("+1"+field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')
        except:
            raise ValidationError('Invalid phone number.')

def validate_facebook(form, field):
    if not 'facebook.com' in field.data:
        raise ValidationError('Invalid facebook link.')

def validate_unique_venue_name(form, field):
    if len(Venue.query.filter(Venue.name==form.name.data).all()) > 0:
        raise ValidationError('A Venue with this name already exists.')

def validate_unique_artist_name(form, field):
    if len(Artist.query.filter(Artist.name==form.name.data).all()) > 0:
        raise ValidationError('A Venue with this name already exists.')

class ShowForm(FlaskForm):
    artist_id = SelectField(
        'Who?', validators=[DataRequired()],
        choices=[('', 'Select an artist')] + 
            [(str(artist.id), artist.name) for artist in Artist.query.all()]
    )
    venue_id = SelectField(
        'Where?', validators=[DataRequired()],
        choices=[('', 'Select a venue')] + 
            [(str(venue.id), venue.name) for venue in Venue.query.all()]
    )
    start_time = DateTimeField(
        'When?',
        validators=[DataRequired()],
        default= datetime.today()
    )
    submit = SubmitField('Submit')

class VenueForm(FlaskForm):
    name = StringField(
        'Name', validators=[DataRequired(), Length(min=3), validate_unique_venue_name]
    )
    city = StringField(
        'City', validators=[DataRequired()]
    )
    state = SelectField(
        'State', validators=[DataRequired()],
        choices=[
            ('', 'Select a state'),
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    address = StringField(
        'Address', validators=[DataRequired()]
    )
    phone = StringField(
        'Phone', validators=[DataRequired(), validate_phone]
    )
    image = StringField(
        'Image', validators=[Optional(), URL()]
    )
    facebook = StringField(
        'Facebook', validators=[Optional(), URL(), validate_facebook]
    )
    website = StringField(
        'Website', validators=[Optional(), URL()]
    )
    isSeeking = BooleanField(
        'Looking for Talent', validators=[]
    )
    seekingDescription = StringField(
        'Seeking Description', validators=[Optional(), Length(min=5, max=255)]
    )
    genres = SelectMultipleField(
        'Genres', validators=[DataRequired()],
        choices=[(str(genre.id), genre.name) for genre in Genre.query.all()]
    )
    submit = SubmitField('Submit')

class ArtistForm(FlaskForm):
    name = StringField(
        'Name', validators=[DataRequired(), validate_unique_artist_name]
    )
    city = StringField(
        'City', validators=[DataRequired()]
    )
    state = SelectField(
        'State', validators=[DataRequired()],
        choices=[
            ('', 'Select a state'),
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    phone = StringField(
        'Phone', validators=[Optional(), validate_phone]
    )
    genres = SelectMultipleField(
        'Genres', validators=[DataRequired()],
        choices=[(str(genre.id), genre.name) for genre in Genre.query.all()]
    )
    image = StringField(
        'Image', validators=[Optional(), URL()]
    )
    facebook = StringField(
        'Facebook', validators=[Optional(), URL(), validate_facebook]
    )
    website = StringField(
        'Website', validators=[Optional(), URL()]
    )
    isSeeking = BooleanField(
        'Seeking Venue'
    )
    seekingDesc = StringField(
        'Seeking Description', validators=[Optional(), Length(min=5, max=255, message='Invalid length.')]
    )
    submit = SubmitField('Submit')

class DeleteForm(FlaskForm):
    id = IntegerField('ID')
    submit = SubmitField('Delete')