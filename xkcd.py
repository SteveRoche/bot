















import requests
from bs4 import BeautifulSoup

start_at = 1
numberOfComics = 10

def main():
	url = "https://xkcd.com/{}"
	imgurl = list()
	imgurl = []
	for i in range(start_at, start_at + numberOfComics) :
		r = requests.get(url.format(i))
		html = r.content
		soup = BeautifulSoup(html, "html.parser")
		imgurl.append("https:" + str(soup.find_all("img")[1]["src"]))
	
	counter = 1
	for url in imgurl : 
		result = requests.get(url, stream=True)
		if result.status_code == 200:
			image = result.raw.read()
			open("Img{}.png".format(counter),"wb+").write(image)
			counter += 1

if _name_ == '_main_':
	main()