import os,sys
from flask import Flask ,request
from pymessenger import Bot

app = Flask(__name__)

Page_token = "EAAQI1W6WkPABABBUcZChoQN461CZBesaadZBZBUoLNrv0KjEWNjFxh5kOWhgGKrZAVhQMczmnh1tDOtQLjDX3M8WgWuEAfAVU4ZCCffxInTYnkdQXFKuH9QJlw2BNRdhlGHQOgqS6SEZA7Qjrsr2IbhbhYfhzZCSP4fiEvAqtZCOveCu4122vq8kk"

Prometheus = Bot(Page_token)

@app.route('/', methods=['GET'])
def verify():
	# Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200

@app.route('/', methods =['POST'])
def webhook():
    data = request.get_json()
    log(data)

    if  data['object'] == 'page':
        for entry in data['entry']:
            for messegeevent in entry['messaging']:

                senderid = messegeevent['sender']['id']
                recipientid = messegeevent['recipient']['id']

                if messegeevent.get('message'):
                    if 'text' in messegeevent['message']:
                        messagetext = messegeevent['message']['text']
                    else:
                        messagetext = 'Empty'

                    reply = messagetext
                    Prometheus.send_text_message(senderid, reply)
    return "ok", 200

def log(message):
    print(message)
    sys.stdout.flush()

if __name__ == "__main__":
    app.run(debug = True , port = 80)

