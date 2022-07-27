import os
import requests
from common.exceptions import BadRequest


def send_otp(to, body):
    url = "https://www.fast2sms.com/dev/bulkV2"
    querystring = {"authorization": os.environ['fas2sms_api'],
                   "message": body,
                   "language": "english",
                   "route": "q",
                   "numbers": str(to)}

    headers = {
        'cache-control': "no-cache"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)
