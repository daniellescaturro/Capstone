import models
import requests
import json
from decimal import *
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required
from utils import getRestaurants

restaurant = Blueprint('restaurants', 'restaurant')

# current directory: '/api/v1/restaurants'

def to_dict(obj):
    if isinstance(obj, dict):
        d = {}
        for (k,v) in obj.items():
            d[k] = to_dict(v)
        return d
    elif isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, list):
        return [to_dict(a) for a in obj]
    else:
        return obj

# READ ROUTE - GET ALL RESTAURANTS
@restaurant.route('/', methods=["GET"])
def get_all_restaurants():
    try:
        aa = list(models.prefetch(models.Restaurant.select(), models.Review.select()))
        restaurants = [to_dict(model_to_dict(restaurant, backrefs=True)) for restaurant in aa]
        return jsonify(data=restaurants, status={"code": 201, "message": "Success"})
    except Exception as e:
        return jsonify(data={}, status={"code": 401, "message": "Error getting resources"})


# READ ROUTE - GET MY RESTAURANTS
@restaurant.route('/mypage', methods=["GET"])
def get_my_restaurants():
    try:
        restaurants = [to_dict(model_to_dict(restaurant)) for restaurant in current_user.restaurants]
        return jsonify(data=restaurants, status={"code": 201, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})


@restaurant.route("/search", methods=["GET"])
def search_restaurant():
    location = request.args.get('location')
    if location:
        token = 'qtRxFBWCo3VmtnTbf95_TbanMIP_5x0ZjqKiGfLqVj12HnSXjULlBNTWfEh8oA4fUkg3_k7REPYg5HmhmJzae5KEqXfSyMeGrAfRBG5Z93hCR_NSdwxXKqWTKxvFX3Yx'
        headers = {'Authorization': f'Bearer {token}'}
        r = requests.get('https://api.yelp.com/v3/businesses/search?categories=restaurant&location={}&limit=50'.format(location), headers=headers)

        payload = r.json()
        data = getRestaurants(payload, current_user)
        return jsonify(data=data, status={"code": 200, "message": "Success"})
    return jsonify(data={}, status={"code": 402, "message": "Success"})

# CREATE ROUTE - POST NEW RESTAURANT
@restaurant.route('/add', methods=["POST"])
def create_restaurant():
    payload = request.get_json()

    restaurant = models.Restaurant.create(
        uploader=current_user.id,
        name=payload['name'],
        image_url=payload['image_url'],
        url=payload['url'],
        review_count=0,
        title=payload['title'],
        rating=payload['rating'],
        address1=payload['address1'],
        city=payload['city'],
        state=payload['state'],
        zip_code=payload['zip_code'],
        heat_lamps=payload['heat_lamps']
    )

    restaurant_dict = model_to_dict(restaurant)
    return jsonify(data=restaurant_dict, status={"code": 201, "message": "Success"})


# SHOW ROUTE
@restaurant.route('/<id>', methods=['GET'])
def get_one_restaurant(id):
    restaurant = models.Restaurant.get_by_id(id)
    return jsonify(data=to_dict(model_to_dict(restaurant, backrefs=True)), status={"code": 200, "message": "Success"})


# UPDATE ROUTE
@restaurant.route('/<id>', methods=["PUT"])
def update_restaurant(id):
    payload = request.get_json()

    query = models.Restaurant.update(**payload).where(models.Restaurant.id==id)
    query.execute()
    restaurant = to_dict(model_to_dict(models.Restaurant.get_by_id(id), backrefs=True))
    return jsonify(data=restaurant, status={"code": 200, "message": "Success"})


# DELETE ROUTE
@restaurant.route('/<id>', methods=["DELETE"])
def delete_restaurant(id):
    delete_query = models.Restaurant.delete().where(models.Restaurant.id==id)
    num_of_rows_deleted = delete_query.execute()
    models.Favorite.delete().where(models.Favorite.restaurant_id == id).execute()
    models.Review.delete().where(models.Review.restaurant_id == id).execute()

    return jsonify(
    data={},
    message="Successfully deleted {} item with id {}".format(num_of_rows_deleted, id),
    status={"code": 200, "message": "Success"}
    )
