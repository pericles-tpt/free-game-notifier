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

from api   import attempt_get_raw_html, attempt_po_api_request
from files import read_lines_to_list, append_to_file
from time  import sleep
import os

MINUTE      = 60
run_every   = 15 * MINUTE
found_deals = []
delim       = '¤'
retry_delay = 30 * MINUTE

def main():
	global found_deals

	try:

		# 1. Restore freebies/bundles/etc from previous sessions, from disk
		# TODO: Come back to this, it might not be effective if there are long period between running this
		all_entries       = read_lines_to_list()
		old_entries_exist = len(all_entries) > 0
		last_found        = all_entries[-1].split('¤')[0] if len(all_entries) > 0 else None
		found             = False

		while(1):
			# 2. Get valid items from raw html
			bundles  = filter_valid_items("https://gg.deals/au/news/bundles")
			freebies = filter_valid_items("https://gg.deals/au/news/freebies")

			if (bundles == None or freebies == None):
				print(f"gg.deals appears to be down, sleeping for {retry_delay/60} minutes before retrying...")
				sleep(retry_delay)
				continue

			# 3. Reset the notification queue
			notify_q  = []

			# 4. Update notify_q and found_deals
			notify_q    += freebies + bundles
			found_deals += freebies + bundles

			# 5. Reverse notify_q to present notifications in the right order
			#    AND write to disk
			notify_q.reverse()
			out_str = ""
			for i in notify_q:
				if (not found and old_entries_exist):
					if (i[0] == last_found):
						found = True
				else:
					out_str += f"{i[0]}{delim}{i[1]}\n"
					attempt_po_api_request(f"{i[1]}: '{i[0]}'")
			append_to_file(out_str)

			sleep(run_every)

	except Exception as e:
		print(f"Error occured: {e}")
		attempt_po_api_request("'Free Game Notifier' has terminated", 1)

def filter_valid_items(url, s_str=">", e_str="</a></h3>"):
	e_str_len = len(e_str)
	data      = attempt_get_raw_html(url)
	if (data == None):
		return data
	ret       = []

	for i in range(e_str_len, len(data)):

		# If a match is found with the end string...
		if (data[i - e_str_len:i] == e_str):

			# Keep going back until a match with s_str is found...
			c = ""
			j = 0
			while (c != s_str):
				c = data[i - e_str_len - j]
				j += 1

			# Determine if it's the desired item... (could put some filters here)
			tup      = None
			item_str = data[i- e_str_len - j+2: i - e_str_len]
			if ("freebies" in url):
				game  = item_str
				store = 'GAME'
				tup = (game, store)
			elif ("bundles" in url):
				game  = item_str
				store = 'BUNDLE'
				tup = (game, store)

			# Send a notification if it hasn't already been found
			if ((tup != None) and (tup not in found_deals)):
				ret.append(tup)
	
	return ret

if __name__ == "__main__":
	main()
