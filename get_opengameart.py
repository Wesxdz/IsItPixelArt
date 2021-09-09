from bs4 import BeautifulSoup
import urllib
import requests

pages = 50

# http = urllib3.PoolManager()

for page in range(0, pages):
    site = "https://opengameart.org/art-search-advanced?keys=&title=&field_art_tags_tid_op=or&field_art_tags_tid=NES%2Cpixel%20art%2C16x16%2C32x32&name=&field_art_type_tid%5B0%5D=9&field_art_licenses_tid%5B0%5D=4&sort_by=score&sort_order=DESC&items_per_page=24&Collection=&page=" + str(page)
    html_doc = urllib.request.urlopen(site)
    soup = BeautifulSoup(html_doc, 'html.parser')
    items = soup.find_all(lambda tag : 'class' in tag.attrs and 'field-item' in tag['class'] and 'property' not in tag.attrs)
    for item in items:
        pack_source = "https://opengameart.org/" + item.a.get('href')
        pack_doc = urllib.request.urlopen(pack_source)
        pack_soup = BeautifulSoup(pack_doc, 'html.parser')
        files = pack_soup.find_all(lambda tag: 'class' in tag.attrs and 'file' in tag['class'])
        for file in files:
            img_source = file.a.get('href')
            if img_source.endswith('png'):
                img_data = requests.get(img_source).content
                filename = img_source.split('/')[-1]
                print(filename)
                open("model/data/yes/opengameart/" + filename, 'wb').write(img_data)
