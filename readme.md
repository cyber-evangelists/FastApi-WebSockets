# Project Description

# Frontend

I have created a react frontend and a python backend, the react frontend sends request to the backend which has to be running at the time of the request, Once the handshake is done the frontend and backend both are connected.

I have used useFormik hook for input validation and sanitizing the input in react frontend.

The handshake is done inside a useEffect hook so that the handshake is done before the components are mounted.

I am sending and receiving data in JSON format, however I am having trouble in recieving non Json data such as messages like Post Inserted.

The data is shown in a table.

# Backend

In the main.py I have created an endpoint using websockets.

I have also integrated mongodb database here, now we can get all posts, search for a specific post and insert a new post into the database.

The code is passing commands like 'add_post' from the frontend, which is then verified inside the web socket endpoint, according to which the function is performed.

We are using ConnectionManager class toestablish a secure web socket connection.

We are using mongodb ObjectID to identify the entries in the database. The user searched id is being converted into ObjectID literal which is then compared to the ObjectID of mongodb.

# How to run

Split the terminal into two
Navigate to frontend in 1st and to backend in 2nd terminal using cd command
run npm start for frontend
run pip install -r requirements.txt in backend
run uvicorn main:app --reload for backend
