from bs4 import BeautifulSoup
from urllib import request
import requests

site = "https://pixeljoint.com"
pages = 84

def iterate_gallery():
    for i in range(1, pages):
        try:
            html_doc = request.urlopen(site + "/pixels/new_icons.asp?q=1&pg=" + str(i))
        except:
            continue
        soup = BeautifulSoup(html_doc, 'html.parser')
        boxes = soup.find_all(lambda tag : 'class' in tag.attrs and 'imgbox' in tag['class'])
        for box in boxes:
            img_doc = request.urlopen(site + box.a.get('href'))
            img_soup = BeautifulSoup(img_doc, 'html.parser')
            pixel_img = img_soup.find(lambda tag: 'id' in tag.attrs and tag['id'] == 'mainimg')
            pixel_img_source = site + pixel_img.get('src')
            img_data = requests.get(pixel_img_source).content
            filename = pixel_img_source.split('/')[-1]
            open("data/yes/pixeljoint/" + filename, 'wb').write(img_data)

iterate_gallery()