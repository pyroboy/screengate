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

import websocket


class GraphQLClient():
    """
    A simple GraphQL client that works over Websocket as the transport
    protocol, instead of HTTP.
    This follows the Apollo protocol.
    https://github.com/apollographql/subscriptions-transport-ws/blob/master/PROTOCOL.md
    """

    def __init__(self, url):
        self.ws_url = url
        self._conn = websocket.create_connection(self.ws_url,
                                                 on_message=self._on_message)
        self._conn.on_message = self._on_message
        self._subscription_running = False
        self._st_id = None

    def _on_message(self, message):
        data = json.loads(message)
        # skip keepalive messages
        if data['type'] != 'ka':
            print(message)

    def _conn_init(self, headers=None):
        payload = {
            'type': 'connection_init',
            'payload': {'headers': headers}
        }
        self._conn.send(json.dumps(payload))
        self._conn.recv()

    def _start(self, payload):
        _id = gen_id()
        frame = {'id': _id, 'type': 'start', 'payload': payload}
        self._conn.send(json.dumps(frame))
        self._conn.recv()
        return _id

    def _stop(self, _id):
        payload = {'id': _id, 'type': 'stop'}
        self._conn.send(json.dumps(payload))
        return self._conn.recv()

    def query(self, query, variables=None, headers=None):
        self._conn_init(headers)
        payload = {'headers': headers, 'query': query, 'variables': variables}
        _id = self._start(payload)
        self._conn.recv()
        res = self._stop(_id)
        #print(dir(self._conn))
        return res

    def subscribe(self, query, variables=None, headers=None, callback=None):
        self._conn_init(headers)
        payload = {'headers': headers, 'query': query, 'variables': variables}
        _cc = self._on_message if not callback else callback
        _id = self._start(payload)
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

    def stop_subscribe(self, _id):
        self._subscription_running = False
        self._st_id.join()
        self._stop(_id)

    def close(self):
        self._conn.close()


# generate random alphanumeric id
def gen_id(size=6, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))



ws = GraphQLClient('ws://hasura-midcodes1.herokuapp.com/v1/graphql')

#add headers

def callback(_id, data):
  print("got new data..")
  print(f"msg id: {_id}. data: {data}")

query = """
subscription {
  scanned(limit: 1, order_by: {created_at: desc}) {`
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




#!/usr/bin/env python3

import sys, json
import asyncio
from websockets import connect

class EchoWebsocket:
    async def __aenter__(self):
        self._conn = connect('wss://ws.binaryws.com/websockets/v3')
        self.websocket = await self._conn.__aenter__()        
        return self

    async def __aexit__(self, *args, **kwargs):
        await self._conn.__aexit__(*args, **kwargs)

    async def send(self, message):
        await self.websocket.send(message)

    async def receive(self):
        return await self.websocket.recv()

class mtest:
    def __init__(self):
        self.wws = EchoWebsocket()
        self.loop = asyncio.get_event_loop()

    def get_ticks(self):
        return self.loop.run_until_complete(self.__async__get_ticks())

    async def __async__get_ticks(self):
        async with self.wws as echo:
            await echo.send(json.dumps({'ticks_history': 'R_50', 'end': 'latest', 'count': 1}))
            return await echo.receive()


            from testws import *

a = mtest()

foo = a.get_ticks()
print (foo)

print ("async works like a charm!")

foo = a.get_ticks()
print (foo)


root@ubupc1:/home/dinocob# python3 test.py
{"count": 1, "end": "latest", "ticks_history": "R_50"}
async works like a charm!
{"count": 1, "end": "latest", "ticks_history": "R_50"}