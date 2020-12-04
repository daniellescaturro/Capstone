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


# READ ROUTE - GET MY FAVORITES
@favorite.route('/myfavorites', methods=["GET"])
def get_my_favorites():
    try:
        favorites = [to_dict(model_to_dict(favorite)) for favorite in current_user.favorites]
        print(favorites)
        return jsonify(data=favorites, status={"code": 201, "message": "Success"})
    except models.DoesNotExist:
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


# BRIAN'S CODE -- SYNTAX ERRORS
# @favorite.route('/<user_id>', methods=["GET"]) 
# def get_my_favorites(user_id): 
#     favorite = models.Favorite.get_by_user_id(user_id) 
#     if favorite.user.id == current_user.id: 
#         favorite_dict = (to_dict(model_to_dict(favorite) )
#         favorite_dict['user'].pop('password')  
#
#         return jsonify( 
#             data=favorite_dict, 
#             message=f"Found status with id: {id}.", 
#             status=200
#         ), 200 
#
#     else:  
#         return jsonify( 
#             data={ 'error': '404 not found' }, 
#             message="You do not have access to this information.", 
#             status=404
#         ), 404 

# READ ROUTE - GET ALL FAVORITES -- DOESN'T WORK
# @favorite.route('/', methods=["GET"])
# def get_all_favorites():
#     try:
#         favorites = [to_dict(model_to_dict(favorite)) for favorite in models.Favorite.select()]
#         print(favorites)
#         return jsonify(data=favorites, status={"code": 201, "message": "Success"})
#     except models.DoesNotExist:
#         return jsonify(data={}, status={"code": 401, "message": "Error getting resources"})


# READ ROUTE - GET MY FAVORITES -- DOESN'T WORK
# @favorite.route('/myfavorites', methods=["GET"])
# def get_my_favorites():
#     try:
#         favorites = [to_dict(model_to_dict(favorite)) for favorite in current_user.favorites]
#         print(favorites)
#         return jsonify(data=favorites, status={"code": 201, "message": "Success"})
#     except models.DoesNotExist:
#         return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})
