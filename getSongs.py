import eyed3
eyed3.log.setLevel("ERROR")
import glob
songs = glob.glob("D:\Music\Pixel Music\*.mp3")
	
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    print(e)

#url = "https://tabs.ultimate-guitar.com/tab/car_seat_headrest/drunk_drivers_killer_whales_chords_1814908"
#html = BeautifulSoup(simple_get(url), 'html.parser')
#for span  in html.select('span'):
#	print(span["class"][0])
	
"""
url = "https://www.billboard.com/charts/artist-100"
html = BeautifulSoup(simple_get(url), 'html.parser')
for div in html.select('div'):
	#print(div["class"][0])
	try:
		song = ""
		artist = ""
		if(div["class"][0] == "chart-list-item"):
			artist = div["data-artist"]
			song = div["data-title"]
					
			try:
				url = "https://www.guitartabs.cc/search.php?tabtype=any&band=" + song.lower().replace(" ", "+") 
				print(url)
				html = BeautifulSoup(simple_get(url), 'html.parser')
				#print(html)
				for tr in html.select('tr'):
					if(tr["class"][0] == "stripe"):
						print(tr["class"][0])
			except:
				pass
	except:
		pass
"""
"""
for song in songs:
	try:
		audiofile = eyed3.load(song)
		url = "https://www.hooktheory.com/theorytab/view/" + audiofile.tag.artist.lower().replace(" ", "+")  + "/"  + audiofile.tag.title.lower().replace(" ", "-")
		print("https://www.hooktheory.com/theorytab/view/" + audiofile.tag.artist.lower().replace(" ", "+")  + "/"  + audiofile.tag.title.lower().replace(" ", "-"))
		html = BeautifulSoup(simple_get(url), 'html.parser')
		#print(html)
		for h in html.select('h1'):
			print(h)
	except:
		pass
"""