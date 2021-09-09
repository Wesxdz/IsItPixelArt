from bs4 import BeautifulSoup
import urllib

samples = 20000
page_size = 500

# http = urllib3.PoolManager()

for offset in range(0, samples, page_size):
    site = "https://commons.wikimedia.org/w/index.php?title=Special:MIMESearch/image/png&limit=" + str(page_size) + "&offset=" + str(offset) + "&mime=image%2Fpng"
    html_doc = urllib.request.urlopen(site)
    soup = BeautifulSoup(html_doc, 'html.parser')
    image_list = soup.find('ol')
    items = image_list.find_all('li')
    for item in items:
        img_source = item.a.get('href')
        print(img_source)
        # img_data = requests.get(img_source).content
        # https://meta.wikimedia.org/wiki/User-Agent_policy
        # headers={"UserAgent", "bot IsItPixelArt/0.0 (https://en.wikipedia.org/wiki/User:Wesxdz; sirwesleybarlow@gmail.com)"}
        filename = item.find_all('a')[1].get('title').split('!')[-1]
        req = urllib.request.Request(img_source)
        req.add_header("User-Agent", "bot IsItPixelArt/0.0 (https://en.wikipedia.org/wiki/User:Wesxdz; sirwesleybarlow@gmail.com)")
        # urllib.request.urlretrieve(req, "model/data/no/wikipedia/" + filename)
        response = urllib.request.urlopen(req)
        # response = http.request("GET", img_source)
        img_data = response.read()
        open("model/data/no/wikipedia/" + filename, 'wb').write(img_data)
