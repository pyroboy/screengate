# -*- coding: utf-8 -*-
import string
import random
import json
import time
import asyncio
from websockets import connect
#import websocket
import time
#import pdb; pdb.set_trace()

class GraphQLClient:
    def connect(self,url,headers = None):
        self.ws_url = url
        self.headers = headers

    async def __aenter__(self):
        print("Connecting")
        self._conn = connect(self.ws_url,subprotocols=['graphql-ws'])
        self.websocket = await self._conn.__aenter__()   
        print("connection done")
        payload = {
            'type': 'connection_init',
            'payload': {'headers': self.headers}
        }
        await self.websocket.send(json.dumps(payload))
        print("connection Initialized")
        return self

    async def __aexit__(self, *args, **kwargs):
        await self._conn.__aexit__(*args, **kwargs)

    async def framePayload(self, payload):
        _id = await gen_id()
        frame = {'id': _id, 'type': 'start', 'payload': payload}
        await self.websocket.send(json.dumps(frame))
        return _id

    async def _stop(self, _id):
        payload = {'id': _id, 'type': 'stop'}
        self._conn.send(json.dumps(payload))
        return await self.websocket.recv()

    async def query(self, query, variables=None, headers=None):
        self._conn_init(headers)
        payload = {'headers': headers, 'query': query, 'variables': variables}
        _id = self.framePayload(payload)
        await self.websocket.recv()
        res = self._stop(_id)
        #print(dir(self._conn))
        return res


    async def stop_subscribe(self, _id):
        print("Subscribe stop")
        self._subscription_running = False
        self._st_id.join()
        self._stop(_id)

    async def subscribe(self, query, variables=None, headers=None, callback=None):

        payload = {'headers': self.headers, 'query': query, 'variables': variables}
        _id = await self.framePayload(payload)
        print("Subscribe payloads Sent")
        print("Listening")
        start_time = time.time()
        self._subscription_running = True
        async for message in self.websocket:
            r = json.loads(message)
            if r['type'] == 'error' or r['type'] == 'complete':
                self.stop_subscribe(_id)
                break
            elif r['type'] != 'ka' and r['type'] != 'connection_ack':
                print(r)
                print("--- %s seconds ---" % (time.time() - start_time))



# generate random alphanumeric id
async def gen_id(size=6, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


#add headers

query = """
subscription {
  scanned(limit: 1, order_by: {created_at: desc}) {
    id
    scan
  }
}
"""

async def gqlClient():
    print("RAT")
    gql = GraphQLClient()
    gql.connect(url = 'ws://hasura-midcodes1.herokuapp.com/v1/graphql',headers = None)
    async with gql as ws:
        id = await ws.subscribe(query)
        return "rat"

async def main():
        await gqlClient()
        print(f'started subscriptions, will keep it alive for {subalive} seconds')
        time.sleep(subalive)
        print(f'{subalive} seconds over, stopping the subscription')
        ws.stop_subscribe(id)
        ws.close()



asyncio.run(main())