import os,sys
from flask import Flask ,request
from witt import wit_response
from pymessenger import Bot

app = Flask(__name__)
# Page token
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

                if messegeevent.get('message'):
                    if 'text' in messegeevent['message']:
                        messagetext = messegeevent['message']['text']
                    else:
                        messagetext = 'Empty'

                    reply = None

                    entity , value = wit_response(messagetext)

                    if entity == 'location':
                        reply = "Oh! {0} a nice place.".format(str(value))
                    elif entity == 'greetings':
                        reply = "Hi There! how can i help you"
                    elif entity == "information":
                        reply = "Sir this is a meme page!"
                    else:
                        reply = "Sorry! I didn't recieve anything"

                    Prometheus.send_text_message(senderid, reply)
    return "ok", 200

def log(message):
    print(message)
    sys.stdout.flush()

if __name__ == "__main__":
    app.run(debug = True , port = 80)

