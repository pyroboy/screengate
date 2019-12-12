from flask import request
from flask import Flask
app = Flask(__name__)

#1: Delivered to phone, 
#2: Non-Delivered to Phone, 
#4: Queued on SMSC, 
#8: Delivered to SMSC, 
#16: Non-Delivered to SMSC.

@app.route('/sms')
def data():
    # here we want to get the value of user (i.e. ?user=some-value)
    #user = request.args.get('message_id')
    #user = request.args.get('status')
    #user = request.args.get('status_text')
    #user = request.args.get('smsc')
    #user = request.args.get('sms_id')
    #user = request.args.get('date_sent')
    #user = request.args.get('identity')

    #print(request.args)
    print()
    return 'OK'


if __name__ == '__main__':
    app.run()