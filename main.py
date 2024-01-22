import uvicorn
from fastapi import FastAPI, WebSocket, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from model import PostSchema
import json


app = FastAPI()

class PostSchema(BaseModel):
    id: int
    title: str
    text: str

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>CRUD</title>
    </head>
    <body>
        <h1>Websocket CRUD</h1>
        <form action="" onsubmit="Read(event)">
            <button id="getpostsbyID">Get all posts</button>
        </form>
        <form action="" onsubmit="getPostById(event)">
            <label for="postId">Enter Post ID:</label>
            <input type="number" id="postId" name="postId" required>

            <button type="submit">Get Post by ID</button>

        </form>
         <form action="" onsubmit="addPost(event)">

            <label for="postId">Enter New Post ID:</label>
            <input type="number" id="postId" name="postId" required>

            <label for="title">Enter Title:</label>
            <input type="text" id="title" name="postId" required>

            <label for="postText">Enter Post:</label>
            <input type="text" id="postText" name="postId" required>

               <button type="submit">Add new post</button>

            
           
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function Read(event) {
                var input = document.getElementById("getpostsbyID")
                ws.send("get_all_posts")
                input.value = ''
                event.preventDefault()
            }
            function getPostById(event) {
                var postId = document.getElementById("postId").value
                ws.send("get_post_by_id:" + postId)
                event.preventDefault()
            }
              function addPost(event) {
                var newpostId = document.getElementById("postId").value
                var newposTitle = document.getElementById("title").value
                var newpostText = document.getElementById("postText").value
           

                 var postData = {
                    command: "add_new_post",
                    postId: newpostId,
                    title: newposTitle,
                    text: newpostText
                };
                ws.send(JSON.stringify(postData));
                event.preventDefault();
          
            }
        </script>
    </body>
</html>
"""

posts = [
    PostSchema(id=1, title="Penguins", text="Penguins are a group of aquatic flightless birds."),
    PostSchema(id=2, title="Tigers", text="Tigers are the largest living cat species and a member of the genus panthera."),
    PostSchema(id=3, title="Koalas", text="Koala is arboreal herbivorous marsupial native to Australia."),
]

users = []
@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        if data == "get_all_posts":
            await websocket.send_text(f"The Posts are {posts}")
        elif data.startswith("get_post_by_id:"):
            post_id = int(data.split(":")[1])
            post = next((p for p in posts if p.id == post_id), None)
            if post:
                await websocket.send_text(f"Post with ID {post_id}: {post}")
            else:
                await websocket.send_text(f"Post with ID {post_id} not found.")

        # elif data.startswith("add_new_post"):
        
         
            
            
