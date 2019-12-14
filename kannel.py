
import requests
import uuid

#####################################
kannelUser= "rapidsms"
kannelPass = "CHANGE-ME"
dlr_url = "http://127.0.0.1:5000/sms"
#####################################

dlr_url_params = ("message_id=%s" % uuid.uuid4(),
                    "status=%d",
                    "status_text=%A",
                    "smsc=%i",
                    "sms_id=%I",
                    "date_sent=%t",
                    "identity=%p")
dlr_url_params = '&'.join(dlr_url_params)

dlr = str(dlr_url+"?"+dlr_url_params)

#validity	number (minutes)	Optional. If given, Kannel will inform SMS Center that it should only try to send the message for this many minutes. If the destination mobile is off other situation that it cannot receive the sms, the smsc discards the message. Note: you must have your Kannel box time synchronized with the SMS Center.
#deferred	number (minutes)
#202	0: Accepted for delivery	The message has been accepted and is delivered onward to a SMSC driver. Note that this status does not ensure that the intended recipient receives the message.
#202	3: Queued for later delivery	The bearerbox accepted and stored the message, but there was temporarily no SMSC driver to accept the message so it was queued. However, it should be delivered later on.
#4xx	(varies)	There was something wrong in the request or Kannel was so configured that the message cannot be in any circumstances delivered. Check the request and Kannel configuration.
#503	Temporal failure, try again later.


async def sendSMS(to,_from,text,smsc="FAKE"):
    p = (
    ('username', kannelUser),
    ('password', kannelPass),
    ('smsc', smsc), 
    ('from', _from),
    ('charset', 'ascii'),
    ('coding', '0'),
    ('dlrmask', '31'),
    ('to', to),
    ('text', text),
       ('dlr-url', dlr ),
    )
    r = requests.get("http://127.0.0.1:13013/cgi-bin/sendsms", params = p)
    if r.status_code == 202:
        smssend_status = r.content.decode("utf-8")[:1]
        if smssend_status == '0':
            return ('\033[95mAccepted for delivery\33[0m')
        if smssend_status == '3':
            return ('\033[95mQueued for later delivery\33[0m')
    else:
        print('\033[91m Kannel Service not found\33[0m')
    print(r.status_code)
    
   




