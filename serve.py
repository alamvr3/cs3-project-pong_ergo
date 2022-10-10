# from http.server import HTTPServer, SimpleHTTPRequestHandler
# import ssl 

# httpd = HTTPServer(('labradoodle.caltech.edu', 7424), SimpleHTTPRequestHandler)
# httpd.socket = ssl.wrap_socket(httpd.socket, certfile='myCA.pem', keyfile='myCA.key', server_side=True)
# httpd.serve_forever()

import asyncio
import websockets
import json

connected = []

async def join(websocket, msg):
    print(msg)
    if(len(connected) == 0):
        connected.append([websocket])
        await websocket.send("waiting for player")
    else:
        added = False
        for games in connected:
            if(len(games) != 2):
                games.append(websocket)
                print(games)
                websockets.broadcast(games, "game ready")
                added = True
        if(added != True):
            connected.append([websocket])
            await websocket.send("waiting for player")
        else

 
async def handler(websocket, path):
    while True:
        msg = await websocket.recv()
        if msg == "join":
            await join(websocket, msg)
        elif "ping" == msg:
            await websocket.send("pong")
        

async def main():
    async with websockets.serve(handler, "labradoodle.caltech.edu", 1234):
        await asyncio.Future()
 
 
if __name__ == "__main__":
    asyncio.run(main())