import models
import requests
import json
from decimal import *
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

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
    else:
        return obj

# READ ROUTE - GET ALL RESTAURANTS
@restaurant.route('/', methods=["GET"])
def get_all_restaurants():
    try:
        restaurants = [to_dict(model_to_dict(restaurant)) for restaurant in models.Restaurant.select()]
        print(restaurants)
        return jsonify(data=restaurants, status={"code": 201, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting resources"})


# READ ROUTE - GET MY RESTAURANTS
@restaurant.route('/mypage', methods=["GET"])
def get_my_restaurants():
    try:
        restaurants = [to_dict(model_to_dict(restaurant)) for restaurant in current_user.restaurants]
        print(restaurants)
        return jsonify(data=restaurants, status={"code": 201, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})


# CREATE ROUTE - POST NEW RESTAURANT
@restaurant.route('/mypage/create', methods=["POST"])
def create_restaurant():
    payload = request.get_json()
    print(type(payload), 'payload')

    restaurant = models.Restaurant.create(
        uploader=current_user.id,
        name=payload['name'],
        image_url=payload['image_url'],
        url=payload['url'],
        review_count=payload['review_count'],
        title=payload['title'],
        rating=payload['rating'],
        address1=payload['address1'],
        city=payload['city'],
        state=payload['state'],
        zip_code=payload['zip_code'],
        heat_lamps=payload['heat_lamps']
    )

    print(restaurant.__dict__)
    print(dir(restaurant))
    print(model_to_dict(restaurant), 'model to dict')
    restaurant_dict = model_to_dict(restaurant)
    return jsonify(data=restaurant_dict, status={"code": 201, "message": "Success"})


# SHOW ROUTE
@restaurant.route('/<id>', methods=['GET'])
def get_one_restaurant(id):
    restaurant = models.Restaurant.get_by_id(id)
    print(restaurant.__dict__)
    return jsonify(data=to_dict(model_to_dict(restaurant)), status={"code": 200, "message": "Success"})


# UPDATE ROUTE
@restaurant.route('/mypage/<id>', methods=["PUT"])
def update_restaurant(id):
    payload = request.get_json()
    print(payload)

    query = models.Restaurant.update(**payload).where(models.Restaurant.id==id)
    query.execute()
    restaurant = to_dict(model_to_dict(models.Restaurant.get_by_id(id)))
    return jsonify(data=restaurant, status={"code": 200, "message": "Success"})


# DELETE ROUTE
@restaurant.route('/mypage/<id>', methods=["Delete"])
def delete_restaurant(id):
    delete_query = models.Restaurant.delete().where(models.Restaurant.id==id)
    num_of_rows_deleted = delete_query.execute()
    print(num_of_rows_deleted)

    return jsonify(
    data={},
    message="Successfully deleted {} item with id {}".format(num_of_rows_deleted, id),
    status={"code": 200, "message": "Success"}
    )


# --------------------------------------
# API pull code
# token = 'qtRxFBWCo3VmtnTbf95_TbanMIP_5x0ZjqKiGfLqVj12HnSXjULlBNTWfEh8oA4fUkg3_k7REPYg5HmhmJzae5KEqXfSyMeGrAfRBG5Z93hCR_NSdwxXKqWTKxvFX3Yx'
# headers = {'Authorization': f'Bearer {token}'}
# r = requests.get('https://api.yelp.com/v3/businesses/search?categories=restaurants&categories=bars&location=brooklyn, ny', headers=headers)
# print(r.json())
# --------------------------------------
