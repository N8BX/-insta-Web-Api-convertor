'''
  _   _  ___  ______   ____   __
 | \ | |/ _ \|  _ \ \ / /\ \ / /
 |  \| | (_) | |_) \ V /  \ V / 
 | . ` |> _ <|  _ < > <    > <  
 | |\  | (_) | |_) / . \  / . \ 
 |_| \_|\___/|____/_/ \_\/_/ \_\
'''

import requests
import re
import base64
import uuid
import random
import string

def print_colored(text, color_code):
    color_codes = {
        'green': '\033[92m',
        'red': '\033[91m',
        'reset': '\033[0m'
    }
    print(f"{color_codes.get(color_code, color_codes['reset'])}{text}{color_codes['reset']}")

sessionID = input("Enter Session Id: ")

if not sessionID or len(sessionID) < 10:
    print_colored("ERROR: Invalid SessionId. Please check the format and try again.", 'red')
else:
    try:
        auth_payload = '{"ds_user_id":"' + sessionID.split("%3A")[0] + '","sessionid":"' + sessionID + '"}'
        encoded_auth = base64.b64encode(auth_payload.encode('utf-8')).decode('utf-8')

        headers = {
            "User-Agent": "Instagram 365.0.0.14.102 Android (28/9; 300dpi; 1600x900; samsung; SM-N975F; SM-N975F; intel; en_US; 373310563)",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "cookie": f"sessionid={sessionID}",
            "X-Bloks-Version-Id": "8ca96ca267e30c02cf90888d91eeff09627f0e3fd2bd9df472278c9a6c022cbb",
            "X-Bloks-Is-Layout-Rtl": "false",
        }

        req = requests.get("https://i.instagram.com/api/v1/accounts/current_user/?edit=true", headers=headers, cookies={"sessionid": sessionID})

        if req.status_code != 200:
            print_colored("ERROR: Invalid SessionId. Please check the format and try again.", 'red')
        else:
            r = req.json()
            mid = req.headers.get("ig-set-x-mid")
            user = r["user"]["username"]

            print_colored(f"[ DONE ] Logged as:@ {user}", 'green')
            headers["X-Mid"] = mid
            print_colored(f"[ DONE ] GET MID: {mid}", 'green')
            print_colored(f"[ @N8BX ] GITHUB&Instagram", 'red')
            print('....')

            data = {}
            data['device_id'] = f"android-{''.join(random.choice('1234567890')for i in range(10))}"
            data['authorization_token'] = f"Bearer IGT:2:{encoded_auth}"

            req = requests.post("https://i.instagram.com/api/v1/accounts/continue_as_instagram_login/", headers=headers, data=data)

            if "logged" in req.text:
                print_colored("[ DONE ] CONVERT !", 'green')
                sess = req.cookies.get("sessionid")
                if sess == None:
                    after = str(base64.b64decode(req.headers.get('ig-set-authorization').split(":")[2]))
                    sess = re.search('"sessionid":"(.*?)"', after).groups()[0]
                print_colored(f"[ API ] Sessionid: {sess}", 'green')
            else:
                print_colored("ERROR: Login failed.", 'red')

    except Exception as e:
        print_colored(f"ERROR: {str(e)}", 'red')