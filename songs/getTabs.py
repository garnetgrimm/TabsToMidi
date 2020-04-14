from selenium import webdriver
import json
import sys
from bs4 import BeautifulSoup
import os

driver = webdriver.PhantomJS()

urls = []
artists = []
songs = []
loss = 0

print("scanning for top artists...")
driver.get("https://www.billboard.com/charts/artist-100")
innerHTML = driver.execute_script("return document.body.innerHTML") #returns the inner HTML as a string
html = BeautifulSoup(innerHTML, 'html.parser')
for element in html.select('div'):
	try:
		#print(element["class"][0])
		if(element["class"][0] == "chart-list-item"):
			artists.append(element["data-title"].strip())
			print("found artist: " + element["data-title"].strip())
	except:
		pass

print("downloading tabs from each artist")
dirname = os.path.dirname(__file__)
dir = os.path.join(dirname, "songs")
if not os.path.exists(dir):
    os.makedirs(dir)
	
for artist in artists:
	driver.get("https://www.ultimate-guitar.com/search.php?search_type=title&value=" + artist.replace(" ", "%20"))
	innerHTML = driver.execute_script("return document.body.innerHTML") #returns the inner HTML as a string
	#print(innerHTML)
	html = BeautifulSoup(innerHTML, 'html.parser')
	urls = []	
	for element in html.select('script'):
		#if(element["class"][0] == "_1YgOS"):
		if (str(element).find("window.UGAPP.store.page =") == -1):
			pass
		else:
			JSON_str = str(element.get_text()).replace("    window.UGAPP.store.i18n = {};", "").replace("    window.UGAPP.store.page = ", "").strip()[:-1]
			#print(JSON)
			JSON = json.loads(JSON_str)
			try:
				for result in JSON['data']['results']:
					try:
						if(result['type'] == "Tabs"):
							song = result['artist_name'] + " - " + result['song_name']
							if song not in songs:
								songs.append(result['artist_name'] + " - " + result['song_name'])
								urls.append(result['tab_url'])
								print("added tab url: " + result['tab_url'])
					except:
						pass
			except:
				pass

			
	for url in urls:
		print("getting data at url: " + url)
		driver.get(url)
		innerHTML = driver.execute_script("return document.body.innerHTML") #returns the inner HTML as a string
		#print(innerHTML)
		from bs4 import BeautifulSoup
		html = BeautifulSoup(innerHTML, 'html.parser')
		for element in html.select('script'):
			#if(element["class"][0] == "_1YgOS"):
			if (str(element).find("window.UGAPP.store.page =") == -1):
				pass
			else:
				JSON_str = str(element.get_text()).replace("    window.UGAPP.store.i18n = {};", "").replace("    window.UGAPP.store.page = ", "").strip()[:-1]
				#print(JSON_str)
				JSON = json.loads(JSON_str)
				dirname = os.path.dirname(__file__)
				filename = os.path.join(dirname, "songs/" + JSON['data']['tab']['song_name'] + ".txt")
				if not os.path.exists(filename):
					f = open(filename, "w")
					try:
						f.write(JSON['data']['tab_view']['wiki_tab']['content'])
					except:
						loss+=1
						print("write failed charmap err")
					print("wrote tab: " + JSON['data']['tab']['song_name'] + ".txt")
				#print(JSON['data']['tab']['song_name'])
				
print("complete, " + str(loss) + " losses")