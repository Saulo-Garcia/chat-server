from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json


app = FastAPI()


@app.get("/")
def read_root():
    return {"massage": "Servidor 2 OnLine "}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connect_clients = []


@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connect_clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                data_json = json.loads(data)
                for client in connect_clients:
                    await client.send_text(json.dumps(data_json))
            except json.JSONDecodeError:
                for client in connect_clients:
                    await client.send_text(data)
    except WebSocketDisconnect:
        connect_clients.remove(websocket)
