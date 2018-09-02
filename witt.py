from wit import Wit
# wit app token
token = "X6RTCACSKTQ23ZBURNE6LNYEJHVEE3BG"

client = Wit(access_token = token )

def wit_response(messagetext):
    responce = client.message(messagetext)
    entity  = None
    value = None

    try:
        entity = list(responce['entities'])[0]
        value = responce['entities'][entity][0]['value']

    except:
        pass
    return (entity,value)

