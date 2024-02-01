from decouple import config
import json
import re
from fastapi import FastAPI, WebSocket, Form, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware
from src.app.connection_manager import ConnectionManager

connection_str = config('uri')
allowed_origin = config('origins')

uri = connection_str 
client = MongoClient(uri, server_api=ServerApi('1'))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[allowed_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
                post_id = data.split(":")[1]
                if re.match('^[a-zA-Z0-9]*$',post_id):
                    try:
                        postid_obj = ObjectId(post_id)
                        result = collection.find_one({"_id": postid_obj})
                        if result:
                            result['_id'] = str(result['_id'])
                            await websocket.send_text(json.dumps(result))
                        else:
                            await websocket.send_text(f"invalid")
                    except:
                        await websocket.send_text(f"not exist")
                        pass
                else:
                    await websocket.send_text(f"validation error")
                    
            elif data.startswith("add_post:"):
                title = data.split(":")[2]  
                newtext = data.split(":")[3]
                if re.match("^[a-zA-Z0-9 ]+$", title) and re.match("^[a-zA-Z0-9 ]+$", newtext):
                    collection = client.get_database().get_collection('test')
                    document = {"title": title, "text": newtext}
                    try:
                       result = collection.insert_one(document)
                       await websocket.send_text("inserted")
                    except Exception as e:
                        await websocket.send_text("insertion error")
                        pass
                else:
                     await websocket.send_text("validation error")
            elif data.startswith("delete_post:"):
                post_id = data.split(":")[1]
                if re.match('^[a-zA-Z0-9]*$',post_id):
                    try:
                        postid_obj = ObjectId(post_id)
                        result = collection.find_one_and_delete({"_id": postid_obj})
                        if result:
                            await websocket.send_text(f"deleted")
                            result = collection.find()
                            for document in result:
                                    document['_id'] = str(document['_id'])
                                    await websocket.send_text(json.dumps(document))
                        else:
                            await websocket.send_text(f"not deleted")
                    except:
                        await websocket.send_text(f"not exist")
                        pass
                else:
                    await websocket.send_text("validation error")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
