from fastapi import FastAPI, WebSocket, Form, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId

uri = "mongodb://localhost:27017/Posts"
client = MongoClient(uri, server_api=ServerApi('1'))

app = FastAPI()

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
            <input type="text" id="postId" name="postId" required>
            <button type="submit">Get Post by ID</button>

        </form>
           <form action="" onsubmit="addPost(event)">
            <label for="title">Enter title:</label>
            <input type="text" id="title" name="newText" required pattern="[A-Za-z\s]+">
            <label for="posttext">Enter post text:</label>
            <input type="text" id="posttext" name="posttext" required pattern="[A-Za-z\s]+">
            <button type="submit">Add a new post</button>

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
            
              var title=document.getElementById("title").value
              var newtext=document.getElementById("posttext").value
              ws.send("add_post:" + ":" + title + ":" + newtext) 
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


users = []
@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
   await manager.connect(websocket)
   collection = client.get_database().get_collection('test')
   try:
        while True:
            data = await websocket.receive_text()
            if data == "get_all_posts": 
                result = collection.find()
                for document in result:
                    await websocket.send_text(f"The Posts are {document}")
            elif data.startswith("get_post_by_id:"):
                post_id = (data.split(":")[1])
                try:
                      postid_obj=ObjectId(post_id)
                      result = collection.find_one({"_id": postid_obj})
                      if result:
                       await websocket.send_text(f"The Posts are {result}")
                      else:
                        await websocket.send_text(f"Post with this ID does not exist")
                except:
                      await websocket.send_text(f"Invalid ID")
            elif data.startswith("add_post:"):
                title = data.split(":")[2]  
                newtext=data.split(":")[3]
                collection = client.get_database().get_collection('test')
                document = { "title": title, "text": newtext}
                try:
                  result = collection.insert_one(document)
                  await websocket.send_text(f"Post inserted successfully")
                except Exception as e:
                 await websocket.send_text(f"Error in insertion")
   except WebSocketDisconnect:
           manager.disconnect(websocket)