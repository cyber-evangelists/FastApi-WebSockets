import json
from pymongo import MongoClient
from pydantic import BaseModel
from bson import json_util

class PostSchema(BaseModel):
    _id: int
    title: str
    text: str

# Your data
posts = [
    PostSchema(_id=1, title="Penguins", text="Penguins are a group of aquatic flightless birds."),
    PostSchema(_id=2, title="Tigers", text="Tigers are the largest living cat species and a member of the genus panthera."),
    PostSchema(_id=3, title="Koalas", text="Koala is an arboreal herbivorous marsupial native to Australia."),
]

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['Posts']
collection = db['Web Socket CRUD']

# Insert data into MongoDB
for post in posts:
    collection.insert_one(post.dict())

# Export data to JSON file
with open('posts.json', 'w') as json_file:
    json.dump(list(collection.find()), json_file, default=json_util.default, indent=4)

client.close()
