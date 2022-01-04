from api  import attempt_get_raw_html, attempt_po_api_request
from time import sleep

MINUTE      = 60
RUN_EVERY   = 15 * MINUTE
found_deals = []

def main():
	global found_deals

	while(1):
		# 1. Get raw html
		data = attempt_get_raw_html("https://gg.deals/au/news/freebies")

		# 2. Go through data char by char (from end to beginning)
		e_str     = "</a></h3>"
		e_str_len = len(e_str)
		s_str     = ">"
		notify_q  = []

		for i in range(e_str_len, len(data)):

			# If a match is found with the end string...
			if (data[i-e_str_len:i] == e_str):

				# Keep going back until a match with s_str is found...
				c = ""
				j = 0
				while (c != s_str):
					c = data[i - e_str_len - j]
					j += 1

				# Determine if it's the desired item... (could put some filters here) 
				item_str = data[i-9-j+2: i-9]
				if (item_str[0:4] == "FREE" and "on" in item_str):
					lst   = item_str[5:].split(' on ')			
					game  = lst[0]
					store = lst[1]
					if (lst[1][:4] == "the "):
						store = lst[1][4:]
					tup = (game, store)

					# Send a notification if it hasn't already been found
					if (tup not in found_deals):
						notify_q.append(tup)
						found_deals.append(tup)
	
		# This reverse() is specific to gg.deals, to get the notifications in the right order
		notify_q.reverse()
		for i in notify_q:
			attempt_po_api_request(f"{i[1]}: '{i[0]}'")

		sleep(RUN_EVERY)

if __name__ == "__main__":
	main()