# -*- coding: utf-8 -*-
"""
A simple GraphQL client that works over Websocket as the transport
protocol, instead of HTTP.
This follows the Apollo protocol.
https://github.com/apollographql/subscriptions-transport-ws/blob/master/PROTOCOL.md
"""

import string
import random
import json
import time
import threading
import asyncio
from websockets import connect


class GraphQLClient:
    async def __aenter__(self, url):
        self.ws_url = url+'ws://hasura-midcodes1.herokuapp.com/v1/graphql'
        self._conn = connect(self.ws_url, on_message=self._on_message)
        self.websocket = await self._conn.__aenter__()   
        self._conn.on_message = self._on_message
        self._subscription_running = False #OK
        self._st_id = None #OK
        return self

    async def __aexit__(self, *args, **kwargs):
            await self._conn.__aexit__(*args, **kwargs)

    async def _on_message(self, message):
        data = await json.loads(message)
        # skip keepalive messages
        if data['type'] != 'ka':
            print(message)

    async def _conn_init(self, headers=None):
        payload = {
            'type': 'connection_init',
            'payload': {'headers': headers}
        }
        await self.websocket.send(json.dumps(payload))
        await self.websocket.recv()

    async def _start(self, payload):
        _id = await gen_id()
        frame = {'id': _id, 'type': 'start', 'payload': payload}
        await self.websocket.send(json.dumps(frame))
        await self.websocket.recv()
        return _id

    async def _stop(self, _id):
        payload = {'id': _id, 'type': 'stop'}
        self._conn.send(json.dumps(payload))
        return await self.websocket.recv()

    async def query(self, query, variables=None, headers=None):
        self._conn_init(headers)
        payload = {'headers': headers, 'query': query, 'variables': variables}
        _id = self._start(payload)
        await self.websocket.recv()
        res = self._stop(_id)
        #print(dir(self._conn))
        return res


    async def stop_subscribe(self, _id):
        self._subscription_running = False
        self._st_id.join()
        self._stop(_id)

    async def subscribe(self, query, variables=None, headers=None, callback=None):
        self._conn_init(headers)
        payload = {'headers': headers, 'query': query, 'variables': variables}
        _cc = await self._on_message if not callback else callback
        _id = await self._start(payload)
        def subs(_cc):
            self._subscription_running = True
            while self._subscription_running:
                r = json.loads(self._conn.recv())
                if r['type'] == 'error' or r['type'] == 'complete':
                    print(r)
                    self.stop_subscribe(_id)
                    break
                elif r['type'] != 'ka':
                    _cc(_id, r)
                time.sleep(1)

        self._st_id = threading.Thread(target=subs, args=(_cc,))
        self._st_id.start()
        return _id




# generate random alphanumeric id
async def gen_id(size=6, chars=string.ascii_letters + string.digits):
    return await ''.join(random.choice(chars) for _ in range(size))



ws = GraphQLClient()

#add headers

def callback(_id, data):
  print("got new data..")
  print(f"msg id: {_id}. data: {data}")

query = """
subscription {
  scanned(limit: 1, order_by: {created_at: desc}) {
    id
    scan
  }
}
"""
subalive = 1000
wait = 40

id = ws.subscribe(query, callback=callback)
print(f'started subscriptions, will keep it alive for {subalive} seconds')
time.sleep(subalive)
print(f'{subalive} seconds over, stopping the subscription')
ws.stop_subscribe(id)
ws.close()