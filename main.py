import requests

# Get raw html
sc = 0
r  = None
while (sc != 200):
	url = "https://gg.deals/au/news/freebies"
	r = requests.get(url)
	sc = r.status_code
text = r.text

game_store = [] # tups: (game, store)
for i in range(9, len(text)):
	if (text[i-9:i] == "</a></h3>"):
		s = ""
		j = 0
		while (s != '>'):
			s = text[i-9-j]
			j += 1
		# We have an item but don't know if it's valid
		item_str = text[i-9-j+2: i-9]
		if (item_str[0:4] == "FREE" and "on" in item_str):
			tmp = item_str[5:].split(' on ')			
			game  = tmp[0]
			store = tmp[1]
			if (tmp[1][:4] == "the "):
				store = tmp[1][4:]
			game_store.append((game, store))

for j in game_store:
	print(f"{game_store.index(j)} {j[1]}: '{j[0]}'")
