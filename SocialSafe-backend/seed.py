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
