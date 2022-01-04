import http.client, urllib.request, requests
from files          import retrieve_from_yaml
from datetime       import datetime
from time           import sleep

timeouts_limit    = 3
timeout           = 30
exception_delay   = 20

# Pushover API - For sending notifications to other devices
def attempt_po_api_request(message):
    po_timeouts_count = 0
    sc                = 0
    conn              = http.client.HTTPSConnection("api.pushover.net:443")

    # Get Key/Token Here
    credentials = retrieve_from_yaml(['PO_USER_KEY', 'PO_TOKEN_KEY'])
    po_user_key = credentials['PO_USER_KEY']
    po_token_key = credentials['PO_TOKEN_KEY']
    
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
    timeout         = 30
    
    # Keep sending the request until we get a status = 200        
    time_start = datetime.now()
    while (sc != 200):

        # Will give up on POSTing to PushOver servers (for this function call) if the "timeout" period elapses
        if ((datetime.now() - time_start).seconds > timeout):
            timeouts_count += 1
            
            # Will skip the rest of this function if n total "timeouts" have occured during the execution of this program
            if timeouts_count == timeouts_limit:
                print(f"PushOver servers may be down, experienced {timeouts_limit} timeouts of POST requests. Skipping notification push...")
                return

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

        return r.text

def handle_exception(error, return_nothing = False):
    print(f"Lost connection, due to '{error}' occured at {datetime.now()}. Wait for {exception_delay} seconds.")
    sleep(exception_delay)

    if not return_nothing:
        return http.client.HTTPSConnection("api.pushover.net:443")