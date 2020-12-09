import requests
import json
import models

token = 'qtRxFBWCo3VmtnTbf95_TbanMIP_5x0ZjqKiGfLqVj12HnSXjULlBNTWfEh8oA4fUkg3_k7REPYg5HmhmJzae5KEqXfSyMeGrAfRBG5Z93hCR_NSdwxXKqWTKxvFX3Yx'
headers = {'Authorization': f'Bearer {token}'}
r = requests.get('https://api.yelp.com/v3/businesses/search?categories=restaurant&location=brooklyn&limit=50', headers=headers)

payloads= r.json()

user = models.User.create(username='admin', email="admin@site.com", password="1234")
for payload in payloads["businesses"]:
    print(json.dumps(payload, indent=4))

    restaurant = models.Restaurant.create(
        uploader=user,
        name=payload['name'],
        image_url=payload['image_url'],
        url=payload['url'],
        review_count=payload['review_count'],
        title=payload['categories'][0]['title'],
        rating=payload['rating'],
        address1=payload['location']['address1'],
        city=payload['location']['city'],
        state=payload['location']['state'],
        zip_code=payload['location']['zip_code']
        )

# SAMPLE DATA
# {
#     "id": "rU9cKxAVU4Gd_JhAqp_bTA",
#     "alias": "buttermilk-channel-brooklyn",
#     "name": "Buttermilk Channel",
#     "image_url": "https://s3-media1.fl.yelpcdn.com/bphoto/veEU8n3he4hWvlyzMo8YAQ/o.jpg",
#     "is_closed": false,
#     "url": "https://www.yelp.com/biz/buttermilk-channel-brooklyn?adjust_creative=gLnJdINJwTgbQ2qDsH1RgQ&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=gLnJdINJwTgbQ2qDsH1RgQ",
#     "review_count": 1891,
#     "categories": [
#         {
#             "alias": "newamerican",
#             "title": "American (New)"
#         },
#         {
#             "alias": "breakfast_brunch",
#             "title": "Breakfast & Brunch"
#         }
#     ],
#     "rating": 4.0,
#     "coordinates": {
#         "latitude": 40.675919,
#         "longitude": -73.999059
#     },
#     "transactions": [
#         "delivery",
#         "pickup"
#     ],
#     "price": "$$",
#     "location": {
#         "address1": "524 Court St",
#         "address2": "",
#         "address3": "",
#         "city": "Brooklyn",
#         "zip_code": "11231",
#         "country": "US",
#         "state": "NY",
#         "display_address": [
#             "524 Court St",
#             "Brooklyn, NY 11231"
#         ]
#     },
#     "phone": "+17188528490",
#     "display_phone": "(718) 852-8490",
#     "distance": 5677.458006391553
# }
