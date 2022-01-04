# PURPOSE: Runs when the main program terminates to send a push notification notifying the user
from api import attempt_po_api_request
attempt_po_api_request("'Free Game Notifier' has terminated", 1)