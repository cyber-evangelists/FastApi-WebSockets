import uvicorn
from fastapi import FastAPI, WebSocket, Form, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
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
            <label for="newId">Enter Post ID:</label>
            <input type="number" id="newId" name="newpostId" required>
            <label for="title">Enter title:</label>
            <input type="text" id="title" name="newText" required>
            <label for="posttext">Enter post text:</label>
            <input type="text" id="posttext" name="posttext" required>
            <button type="submit">Get Text</button>

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
            function addPost(event)
            {
              var newpostId = document.getElementById("newId").value
              var title=document.getElementById("title").value
              var newtext=document.getElementById("posttext").value
              ws.send("add_post:" + newpostId + ":" + title + ":" + newtext) 
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


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
   await manager.connect(websocket)
   try:
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

            elif data.startswith("add_post:"):
                newpostId = int(data.split(":")[1])
                title = data.split(":")[2]  
                newtext=data.split(":")[3]
                
                new_post = PostSchema(id=newpostId, title=title, text=newtext)

                
                posts.append(new_post)

                await websocket.send_text(f"Post added: {new_post}")

   except WebSocketDisconnect:
        manager.disconnect(websocket)

        
         
            
            
