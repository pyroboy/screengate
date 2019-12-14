# -*- coding: utf-8 -*-

# Non - Essential
import time
import string
import random

# Essential
import json
import asyncio
from websockets import connect


#TODO implement Timeout Error

"""
SAMPLE HEADER
initPayload: {
    'headers': json.encode({
    'Authorization': 'Bearer ${token.data}',
    'content-type': "application/json"
    })

"""
gql_Scans_Sub = """
subscription {
  scanned(limit: 1, order_by: {created_at: desc}) {
    id
    scan
  }
}
"""

queue = asyncio.Queue()
is_on_queue = False

async def main():
    url = 'ws://hasura-midcodes1.herokuapp.com/v1/graphql'
    headers = None
    client = await gql_client(url,headers)
    print("\033[92mconnection successful\33[0m")
    _id = await query(client,gql_Scans_Sub)
    print("subscribe command sent")
    print("listening")
    await listen_loop(client)
    await end_query(client, _id)

async def query(client,query,headers=None,variables=None):
    #Random ID generator
    random_id = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
    payload = {'headers': headers, 'query': query, 'variables': variables}
    frame = {'id': random_id, 'type': 'start', 'payload': payload}
    await client.send(json.dumps(frame))
    return random_id

async def end_query(client, _id):
    client.send(json.dumps({'id': _id, 'type': 'stop'}))

async def listen_loop(client):
    async for message in client:
        r = json.loads(message)
        if r['type'] == 'error' or r['type'] == 'complete':
            payload = {'id': _id, 'type': 'stop'}
            client.send(json.dumps(payload))
            break
        elif r['type'] != 'ka' and r['type'] != 'connection_ack':
            if is_on_queue:
                await queue.put(r)
            #print(r)

async def gql_client(url,headers=None):
    client = await connect(url,subprotocols=['graphql-ws'])
    payload = {'type': 'connection_init','payload': {'headers': headers}}
    await client.send(json.dumps(payload))
    return client

#asyncio.run(main())