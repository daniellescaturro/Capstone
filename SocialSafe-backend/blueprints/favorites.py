import models
import json
from decimal import *
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

favorite = Blueprint('favorites', 'favorite')

# current directory: '/api/v1/favorites'

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


# READ ROUTE - GET ALL FAVORITES
@favorite.route('/', methods=["GET"])
def get_all_favorites():
    try:
        favorites = [to_dict(model_to_dict(favorite_to_add)) for favorite_to_add in models.Favorite.select()]
        print(favorites)
        return jsonify(data=favorites, status={"code": 201, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting resources"})

# READ ROUTE - GET MY FAVORITES
@favorite.route('/myfavorites', methods=["GET"])
def get_my_favorites():
    try:
        favorites = [to_dict(model_to_dict(favorite)) for favorite in current_user.favorites]

        return jsonify(data=favorites, status={"code": 201, "message": "Success"})
    except models.DoesNotExist as e:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})


# CREATE ROUTE - POST NEW FAVORITE
@favorite.route('/<restaurant_id>', methods=["POST"])
def create_favorite(restaurant_id):
    payload = request.get_json()
    print(type(payload), 'payload')

    favorite = models.Favorite.create(
        restaurant_id=restaurant_id,
        uploader=current_user.id,
        favorite=payload['favorite']
    )

    print(favorite.__dict__)
    print(dir(favorite))
    print(to_dict(model_to_dict(favorite)), 'model to dict')
    favorite_dict = to_dict(model_to_dict(favorite))
    return jsonify(data=favorite_dict, status={"code": 201, "message": "Success"})

# UPDATE ROUTE
@favorite.route('/<id>', methods=["PUT"])
def update_favorite(id):
    payload = request.get_json()
    print(payload)

    query = models.Favorite.update(**payload).where(models.Favorite.id==id)
    query.execute()
    review = to_dict(model_to_dict(models.Favorite.get_by_id(id)))
    return jsonify(data=review, status={"code": 200, "message": "Success"})

# DELETE ROUTE
@favorite.route('/<id>', methods=["Delete"])
def delete_favorite(id):
    delete_query = models.Favorite.delete().where(models.Favorite.id==id)
    num_of_rows_deleted = delete_query.execute()
    print(num_of_rows_deleted)

    return jsonify(
    data={},
    message="Successfully deleted {} item with id {}".format(num_of_rows_deleted, id),
    status={"code": 200, "message": "Success"}
    )
