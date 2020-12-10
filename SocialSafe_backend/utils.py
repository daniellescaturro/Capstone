from .models import Restaurant
from playhouse.shortcuts import model_to_dict

def getRestaurants(payloads, user):
    return [dict(
        uploader=model_to_dict(user),
        name=payload['name'],
        image_url=payload['image_url'],
        reviews=[],
        favorites=[],
        url=payload['url'],
        review_count=payload['review_count'],
        title=payload['categories'][0]['title'],
        rating=payload['rating'],
        address1=payload['location']['address1'],
        city=payload['location']['city'],
        state=payload['location']['state'],
        zip_code=payload['location']['zip_code']
        ) for payload in payloads["businesses"]]
