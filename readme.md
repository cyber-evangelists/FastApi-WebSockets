# Project Description

In the main.py I have created an endpoint using websockets.

I have also integrated mongodb database here, now we can get all posts, search for a specific post and insert a new post into the database.

The code is passing commands like 'add_post' from the html template, which is then verified inside the web socket endpoint, according to which the function is performed.

We are using ConnectionManager class toestablish a secure web socket connection.

We are using mongodb ObjectID to identify the entries in the database. The user searched id is being converted into ObjectID literal which is then compared to the ObjectID of mongodb.

#How to run
pip install -r requirements.txt

uvicorn main:app --reload
