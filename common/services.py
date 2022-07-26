from twilio.rest import Client
import requests
# Your Account SID from twilio.com/console
# account_sid = "AC406c9f456a9275d7d3a66344c053eca7"
# auth_token = "d78fd1f23ba63de1205abbfac23b3623"
# client = Client(account_sid, auth_token)


# def send_otp(to, body):
#     message = client.messages.create(
#         to=to,
#         from_="+18434387495",
#         body=body)
#     print(message.sid)

def send_otp(to, body):
    url = "https://www.fast2sms.com/dev/bulkV2"

    querystring = {"authorization": "qpO4uwJhAMyZWeDSVvgtUC5cH7fNsTPXFxzb2lGjQ1i80rnE3abscB472Z6GOgVktxEYQhTFSlRen5Mm",
                   "message": body,
                   "language": "english",
                   "route": "q",
                   "numbers": str(to)}

    headers = {
        'cache-control': "no-cache"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)
