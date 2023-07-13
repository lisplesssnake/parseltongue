from bs4 import BeautifulSoup
import requests

URL = 'http://localhost/out.html'	# retirejs html output here

page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

results = soup.find_all("tr",class_="vulnerable")

#print(results.prettify())

for r in results:
    data = r.find_all("td")
    print(data[0].text + '\t--\t' + data[1].text)
    #print(data[1].text)
