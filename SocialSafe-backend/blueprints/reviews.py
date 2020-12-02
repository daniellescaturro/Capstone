import models
import json
from decimal import *
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

review = Blueprint('reviews', 'review')

# current directory: '/api/v1/reviews'

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

# READ ROUTE - GET ALL REVIEWS
@review.route('/', methods=["GET"])
def get_all_reviews():
    try:
        reviews = [to_dict(model_to_dict(review)) for review in models.Review.select()]
        print(reviews)
        return jsonify(data=reviews, status={"code": 201, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting resources"})


# READ ROUTE - GET MY REVIEWS
@review.route('/mypage', methods=["GET"])
def get_my_reviews():
    try:
        reviews = [to_dict(model_to_dict(reviews)) for review in current_user.reviews]
        print(reviews)
        return jsonify(data=reviews, status={"code": 201, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})


# CREATE ROUTE - POST NEW REVIEW
@review.route('/<restaurantid>', methods=["POST"])
def create_review(restaurantid):
    payload = request.get_json()
    print(type(payload), 'payload')

    review = models.Review.create(
        uploader=current_user.id,
        id=restaurantid,
        rating=payload['rating'],
        social_distancing_rating=payload['social_distancing_rating'],
        comments=payload['comments']
    )

    print(review.__dict__)
    print(dir(review))
    print(model_to_dict(review), 'model to dict')
    review_dict = model_to_dict(review)
    return jsonify(data=review_dict, status={"code": 201, "message": "Success"})


# SHOW ROUTE - IS THIS NEEDED
@review.route('/<id>', methods=['GET'])
def get_one_review(id):
    review = models.Review.get_by_id(id)
    print(review.__dict__)
    return jsonify(data=to_dict(model_to_dict(review)), status={"code": 200, "message": "Success"})


# UPDATE ROUTE
@review.route('/<id>', methods=["PUT"])
def update_review(id):
    payload = request.get_json()
    print(payload)

    query = models.Review.update(**payload).where(models.Review.id==id)
    query.execute()
    review = to_dict(model_to_dict(models.Review.get_by_id(id)))
    return jsonify(data=review, status={"code": 200, "message": "Success"})


# DELETE ROUTE
@review.route('/mypage/<id>', methods=["Delete"])
def delete_review(id):
    delete_query = models.Review.delete().where(models.Review.id==id)
    num_of_rows_deleted = delete_query.execute()
    print(num_of_rows_deleted)

    return jsonify(
    data={},
    message="Successfully deleted {} item with id {}".format(num_of_rows_deleted, id),
    status={"code": 200, "message": "Success"}
    )
