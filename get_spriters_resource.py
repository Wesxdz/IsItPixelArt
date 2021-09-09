from bs4 import BeautifulSoup
from urllib import request
import requests

global visited
visited = set()

def iterate_games(url):
    visited.add(url)
    try:
        html_doc = request.urlopen(url)
    except:
        return
    soup = BeautifulSoup(html_doc, 'html.parser')
    games = soup.find(lambda tag: "id" in tag.attrs and tag["id"] == "category-container").findNextSibling()
    for game in games.find_all('a'):
        print(site + game.get('href'))
        download_recursive_img_in_target(site + game.get('href'), "sheet-container")



def download_recursive_img_in_target(url, target):
    """Download img elements contained in every recursive div with @target id :)"""
    visited.add(url)
    try:
        html_doc = request.urlopen(url)
    except:
        return
    soup = BeautifulSoup(html_doc, 'html.parser')
    content = soup.find(lambda tag: "id" in tag.attrs and tag["id"] == "content")
    if content is None:
        return
    for section in content.find_all(lambda tag : "class" in tag.attrs and 'section' in tag["class"]):
        next = section.find_next_sibling()
        for great in next.find_all('a'):
            sheet_page = site + great.get('href')
            try:
                sheet_doc = request.urlopen(sheet_page)
            except:
                continue
            sheet_soup = BeautifulSoup(sheet_doc, 'html.parser')
            for found in sheet_soup.find_all(lambda tag: "id" in tag.attrs and tag.attrs["id"] == target):
                img_url = site + found.img.get('src')
                img_data = requests.get(img_url).content
                filename = img_url.split('/')[-1].split('?')[0]
                open("data/yes" + filename, 'wb').write(img_data)
                print(site + found.img.get('src'))
            
        
    # for link in content.find_all('a'):
    #     suburl = link.get('href')
    #     if suburl not in visited:
    #         # need more specific queries otherwise there are just too many links...
    #         download_recursive_img_in_target(suburl, target)
    # for found in content.findAll(lambda tag: "id" in tag.attrs and tag.attrs["id"] == target):
    #     print("https://www.spriters-resource.com/" + found.img.get('src'))

site = "https://www.spriters-resource.com"
platforms = ["game_boy_advance"] # nes
for platform in platforms:
    html_doc = request.urlopen(site + "/" + platform)
    soup = BeautifulSoup(html_doc, 'html.parser')
    letters = soup.find(lambda tag: tag.get("id") == "letters")
    categories = letters.find_all('a')
    for category in categories:
        print(site + category.get('href'))
        iterate_games(site + category.get('href'))
        # download_recursive_img_in_target(site + category.get('href'), "sheet-container")

# download_recursive_img_in_target("https://www.spriters-resource.com/nes/2ndsuperrobotwarsjpn/", "sheet-container")

print("Complete!")
