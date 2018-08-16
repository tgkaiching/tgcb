import asyncio
import websockets

async def hello():
    async with websockets.connect(
            'ws://adfs.sts.towngas.com/adfs/ls/?wa=wsignin1.0&wtrealm=https%3a%2f%2fitsm.towngas.com%2f&wctx=rm%3d0%26id%3dpassive%26ru%3d%252fdefault.html&wct=2018-08-01T04%3a15%3a16Z"') as websocket:
        name = input("What's your name? ")

        await websocket.send(name)
        print(f"> {name}")

        greeting = await websocket.recv()
        print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())