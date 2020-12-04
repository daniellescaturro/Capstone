from peewee import *
import datetime
import os
from flask_login import UserMixin
from playhouse.db_url import connect


if 'ON_HEROKU' in os.environ:
    # later we will manually add this env var
    # in heroku so we can write this code

    DATABASE = connect(os.environ.get('DATABASE_URL'))
        # heroku will add this
        # env var for you
        # when you provision the
        # Heroku Postgres Add-on
else:
    DATABASE = SqliteDatabase('restaurants.sqlite')


class User(UserMixin, Model):
    username=CharField(unique=True)
    email=CharField(unique=True)
    password=CharField()

    class Meta:
        database = DATABASE


class Restaurant(Model):
    uploader = ForeignKeyField(User, backref='restaurants')
    name = CharField()
    image_url = CharField()
    url = CharField()
    review_count = SmallIntegerField()
    title = CharField()
    rating = DecimalField(2,1)
    address1 = CharField()
    city = CharField()
    state = CharField()
    zip_code = SmallIntegerField()
    heat_lamps = BooleanField(default=False)
    DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE

    def from_yelp(cls, yelp_record):
        return cls()


class Review(Model):
    restaurant_id = ForeignKeyField(Restaurant, backref='reviews')
    uploader = ForeignKeyField(User, backref='reviews')
    rating = DecimalField(2,1)
    social_distancing_rating = DecimalField(2,1)
    comments = CharField()
    DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE


class Favorite(Model):
    restaurant_id = ForeignKeyField(Restaurant, backref='favorite')
    uploader = ForeignKeyField(User, backref='favorite')
    favorite = BooleanField(default=False)

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Restaurant, Review, Favorite], safe=True)
    print("TABLES Created")
    DATABASE.close()
