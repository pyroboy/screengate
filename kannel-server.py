
import requests
import uuid
#
#
# LISTEN to WEBSOCKET
#  POST by WEBSOCKET
#
#
# FASTAPI to KANNEL
#
#   POST to KANNEL URL with PARAMS
#   GET from KANNEL URL with PARAMS
#
#
# sample get-url = http://127.0.0.1:8000/backend/kannel-fake-smsc/?id=%p&text=%a&charset=%C&coding=%c

# "sendsms_url": "http://127.0.0.1:13013/cgi-bin/sendsms",
#        "sendsms_params": {"smsc": "usb0-modem",
#                           "from": "+SIMphonenumber", # not set automatically by SMSC
#                           "username": "rapidsms",
#                           "password": "CHANGE-ME"},
#
#
#	sudo gedit /etc/kannel/kannel.conf
#	sudo gedit /etc/kannel/modem.conf
#
#

#check settings


kannelUser= "rapidsms"
kannelPass = "CHANGE-ME"

# DELIVERY
#            query['dlr-mask'] = 31
#            dlr_url_params = ("message_id=%s" % id_,
#                              "status=%d",
#                              "status_text=%A",
#                              "smsc=%i",
#                              "sms_id=%I",
#                              "date_sent=%t",
#                              "identity=%p")
#dlrmask=31
#text=Event
#to=%2BXXXXXXXX
dlr_url = "http://127.0.0.1:5000/sms"
dlr_url_params = ("message_id=%s" % uuid.uuid4(),
                    "status=%d",
                    "status_text=%A",
                    "smsc=%i",
                    "sms_id=%I",
                    "date_sent=%t",
                    "identity=%p")
dlr_url_params = '&'.join(dlr_url_params)

dlr = str(dlr_url+"?"+dlr_url_params)
print(dlr )
p = (
    ('username', kannelUser),
    ('password', kannelPass),
    ('smsc', 'FAKE'), 
    ('from', '11239'),
    ('charset', 'ascii'),
    ('coding', '0'),
    ('dlrmask', '31'),
 
    ('to', '12223'),
    ('text', 'ping-kannel'),
       ('dlr-url', dlr ),
    )
r = requests.get("http://127.0.0.1:13013/cgi-bin/sendsms", params = p)
if r.status_code != requests.codes.ok:
    r.raise_for_status()
print (r.url)   
print (r.status_code)   
print (r.content)   




