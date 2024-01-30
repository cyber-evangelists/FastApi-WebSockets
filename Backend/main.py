from decouple import config
from fastapi import FastAPI, WebSocket, Form, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware



connection_str = config('uri')
allowed_origin=config('origins')

uri = connection_str 
client = MongoClient(uri, server_api=ServerApi('1'))
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[allowed_origin], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
                      document['_id'] = str(document['_id'])
                      await websocket.send_text(json.dumps(document))
            elif data.startswith("get_post_by_id:"):
                post_id = (data.split(":")[1])
                try:
                      print("hello from try")
                      postid_obj=ObjectId(post_id)
                      print('hello below')
                      print(postid_obj)
                      result = collection.find_one({"_id": postid_obj})
                      if result:
                       result['_id'] = str(result['_id'])
                       await websocket.send_text(json.dumps(result))
                      else:
                          await websocket.send_text(f"invalid")
                except:
                    await websocket.send_text(f"not exist")
                    pass
            
            elif data.startswith("add_post:"):
                title = data.split(":")[2]  
                newtext=data.split(":")[3]
                collection = client.get_database().get_collection('test')
                document = { "title": title, "text": newtext}
                try:
                  result = collection.insert_one(document)
                  await websocket.send_text("inserted")
                except Exception as e:
                 await websocket.send_text(f"insertion error")
                 pass
            elif data.startswith("delete_post:"):
                post_id = (data.split(":")[1])
                try:
                      postid_obj=ObjectId(post_id)
                      result = collection.find_one_and_delete({"_id": postid_obj})
                      if result:
                        await websocket.send_text(f"deleted")
                      else:
                        await websocket.send_text(f"not deleted")
                          
                except:
                    await websocket.send_text(f"not exist")
                    pass
   except WebSocketDisconnect:
           manager.disconnect(websocket)