# Copyright (c) 2022 Pericles Telemachou

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.

import http.client, urllib.request, requests
from files          import retrieve_from_yaml
from datetime       import datetime
from time           import sleep

timeouts_limit    = 3
timeout           = 30
exception_delay   = 20

# Pushover API - For sending notifications to other devices
def attempt_po_api_request(message, token_no=0):
    po_timeouts_count = 0
    sc                = 0
    conn              = http.client.HTTPSConnection("api.pushover.net:443")

    # Get Key/Token Here
    credentials = retrieve_from_yaml(['PO_USER_KEY', 'PO_TOKEN_KEY'])
    po_user_key = credentials['PO_USER_KEY']

    po_token_key = credentials['PO_TOKEN_KEY']
    if (token_no == 1):
        po_token_key = retrieve_from_yaml(['PO_TOKEN_KEY_FAIL'])['PO_TOKEN_KEY_FAIL']
    
    # Keep sending the request until we get a status = 200        
    time_start = datetime.now()
    while (sc != 200):

        # Will give up on POSTing to PushOver servers (for this function call) if the "timeout" period elapses
        if ((datetime.now() - time_start).seconds > timeout):
            po_timeouts_count += 1
            
            # Will skip the rest of this function if n total "timeouts" have occured during the execution of this program
            if po_timeouts_count == timeouts_limit:
                print(f"PushOver servers may be down, experienced {timeouts_limit} timeouts of POST requests. Skipping notification push...")
                return

        try:
            conn.request("POST", "/1/messages.json",
            urllib.parse.urlencode({
                "token": po_token_key,
                "user": po_user_key,
                "message": message,
            }), { "Content-type": "application/x-www-form-urlencoded" })
            sc = conn.getresponse().status
        except Exception as e:
            conn = handle_exception(e)

def attempt_get_raw_html(url):
    timeouts_count  = 0
    sc              = 0
    r               = None

    # Keep sending the request until we get a status = 200
    time_start = datetime.now()
    while (sc != 200):

        # Will give up on POSTing to PushOver servers (for this function call) if the "timeout" period elapses
        if ((datetime.now() - time_start).seconds > timeout):
            timeouts_count += 1

            # Will skip the rest of this function if n total "timeouts" have occured during the execution of this program
            if timeouts_count == timeouts_limit:
                print(f"Couldn't get html, experienced {timeouts_limit} timeouts of GET requests. Skipping get requests...")
                break

        try:
            r    = requests.get(url)
            sc   = r.status_code
        except requests.exceptions.ChunkedEncodingError:
            handle_exception("requests: ChunkedEncodingError", True)
        except requests.exceptions.ConnectionError:
            handle_exception("requests: ConnectionError", True)
        except requests.exceptions.ReadTimeout:
            handle_exception("requests: ReadTimeout", True)
        except requests.exceptions.ConnectTimeout:
            handle_exception("requests: ConnectTimeout", True)
        except Exception as e:
            handle_exception(e)

    try:
        return r.text
    except:
        return None

def handle_exception(error, return_nothing = False):
    print(f"Lost connection, due to '{error}' occured at {datetime.now()}. Wait for {exception_delay} seconds.")
    sleep(exception_delay)

    if not return_nothing:
        return http.client.HTTPSConnection("api.pushover.net:443")
