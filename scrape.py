from bs4 import BeautifulSoup
import requests
import re

URL = 'http://localhost/out.html'

page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

results = soup.find_all("tr",class_="vulnerable")

regex = "(?<=Found in)(.*)(?=- Vulnerability info)"

for r in results:
    data = r.find_all("td")
    x = re.search(regex,data[2].text)
    print((data[0].text).ljust(30) + (data[1].text).ljust(30) + (x[0]).ljust(30))
    print()
