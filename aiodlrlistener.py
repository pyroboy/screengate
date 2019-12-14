from aiohttp import web
import asyncio
import aiowebsocket
import kannel

queue = aiowebsocket.queue
aiowebsocket.is_on_queue = True

async def method(request):
    params = ['message_id',
              'status',
              #'status_text',
              #'smsc',
              #'sms_id',
              'date_sent',
              'identity', ]
    # Get all request into a result dict
    result = { i : request.rel_url.query[i] for i in params }
    # Loop identify status
    for key in SC:
        if key == result['status']:
            print(SC[key]+" -- "+result['date_sent'])
    # Must return something
    return web.Response(text="OK")

async def listen_to_websocket(app):
    url = 'ws://hasura-midcodes1.herokuapp.com/v1/graphql'
    headers = None
    client = await aiowebsocket.gql_client(url,headers)
    print("\33[32m\33[1m**Connection successful!!**\33[0m")
    _id = await aiowebsocket.query(client,aiowebsocket.gql_Scans_Sub)
    print("\033[94m--Query accepted--\33[0m")
    await aiowebsocket.listen_loop(client)
    #await aiowebsocket.end_query(client, _id)

async def worker(app):
    while True:
        value = await queue.get()
        print(value['payload']['data']['scanned'])
        #print(value)
        init_status = await kannel.sendSMS(to="11231",_from="12312312",text="raaaat")
        print(init_status)
        #print("rata")


async def start_background_tasks(app):
    app['scans_listener'] = asyncio.create_task(listen_to_websocket(app))
    app['worker'] = asyncio.create_task(worker(app))

    

async def cleanup_background_tasks(app):
    app['scans_listener'].cancel()
    app['worker'].cancel()
    await app['scans_listener']
    await app['worker']


   
SC= {'1': '\033[92mSuccessfully Sent\33[0m', 
'2': 'Non-Delivered to Phone', 
'4': 'Queued on SMSC', 
'8': '\033[92mSending...\33[0m', 
'16': 'Non-Delivered to SMSC.'}


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

    UNDERLINE = '\033[4m'
    CEND      = '\33[0m'
    CBOLD     = '\33[1m'
    CITALIC   = '\33[3m'
    CURL      = '\33[4m'
    CBLINK    = '\33[5m'
    CBLINK2   = '\33[6m'
    CSELECTED = '\33[7m'

    CBLACK  = '\33[30m'
    CRED    = '\33[31m'
    CGREEN  = '\33[32m'
    CYELLOW = '\33[33m'
    CBLUE   = '\33[34m'
    CVIOLET = '\33[35m'
    CBEIGE  = '\33[36m'
    CWHITE  = '\33[37m'

    CBLACKBG  = '\33[40m'
    CREDBG    = '\33[41m'
    CGREENBG  = '\33[42m'
    CYELLOWBG = '\33[43m'
    CBLUEBG   = '\33[44m'
    CVIOLETBG = '\33[45m'
    CBEIGEBG  = '\33[46m'
    CWHITEBG  = '\33[47m'

    CGREY    = '\33[90m'
    CRED2    = '\33[91m'
    CGREEN2  = '\33[92m'
    CYELLOW2 = '\33[93m'
    CBLUE2   = '\33[94m'
    CVIOLET2 = '\33[95m'
    CBEIGE2  = '\33[96m'
    CWHITE2  = '\33[97m'

    CGREYBG    = '\33[100m'
    CREDBG2    = '\33[101m'
    CGREENBG2  = '\33[102m'
    CYELLOWBG2 = '\33[103m'
    CBLUEBG2   = '\33[104m'
    CVIOLETBG2 = '\33[105m'
    CBEIGEBG2  = '\33[106m'
    CWHITEBG2  = '\33[107m'
    
print(chr(27) + "[2J")
app = web.Application()
app.on_startup.append(start_background_tasks)
app.on_cleanup.append(cleanup_background_tasks)
app.router.add_route('GET', "/sms", method)
web.run_app(app,host='localhost', port=5000)
