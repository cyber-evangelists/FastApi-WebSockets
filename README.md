# Project Description

In the main.py I have created an endpoint using websockets, right now in the endpoint all posts can be shown and specific posts can be retrieved based on their id, Now I can also append in the blogs by using this code. Further I have used the connection manager class which handles the connection, disconnection of a socket.

#How to run
pip install -r requirements.txt

uvicorn main:app --reload
