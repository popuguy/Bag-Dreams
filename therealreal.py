import shutil

from selenium import webdriver
from bs4 import BeautifulSoup

import requests

import time


def csv_append_save(sets, filename):
    """
    Non-destructive multipurpose data saver that appends to a file (creating it if need be)

    :param sets: Set of sets of data to append and save
    :param filename: Filname to append to
    """
    csvized_data = '\n'.join([','.join([str(v) for v in s]) for s in sets]) + '\n'
    f = open(filename, 'a', encoding='utf-8')
    f.write(csvized_data)
    f.close()


def get_and_save_realreal_image_links(driver, realreal_listing_page_url, save_file):
    # Open page in test browser
    driver.get(realreal_listing_page_url)

    # Superstitious additional wait
    driver.implicitly_wait(0.5)

    if "Please click and hold the button" in driver.page_source:
        input("Are we good to continue scraping?")

    # Get source
    pg_src = driver.page_source

    # Parse source
    soup = BeautifulSoup(pg_src, 'html.parser')

    new_bags = []
    for div in soup.find_all("div", {"class": "product-card-aligner"}):
        brand = div.find("div", {"class": "product-card__brand"}).text
        name = div.find("div", {"class": "product-card__description"}).text

        img = div.find_all("img")[0]
        file_link = None
        if ' src=' in str(img) and 'data:image' not in str(img['src']):
            file_link = img['src']
        else:
            file_link = img['data-src']
        if '?' in file_link:
            corrected_res_link = file_link[:file_link.index('?')] + "?width=512"
            new_bags.append([brand, name, corrected_res_link])

    csv_append_save(new_bags, save_file)


def save_binary_from_url(url, save_loc):
    """
    Saves the binary data downloaded from a URL to a destination file
    :param url: URL to download file from
    :param save_loc: Location to save -- must contain file extension
    """
    response = requests.get(url, stream=True)
    with open(save_loc, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response


if __name__ == '__main__':
    webdriver_path = 'insert-your-path'
    chromedriver = webdriver.Chrome(executable_path=webdriver_path)

    listing_file = open('realreallistings.txt', 'r')
    listings = [listing for listing in listing_file.read().split('\n') if 'http' in listing]

    for realreallisting in listings:
        get_and_save_realreal_image_links(chromedriver, realreallisting, 'realrealbaglinks.csv')

    f = open("realrealbaglinks.csv", 'r', encoding='utf-8', errors="surrogateescape")
    contents = f.read()
    f.close()

    csv_lines = contents.split('\n')
    for i in range(len(csv_lines)):
        # print(line.split(',')[2])
        save_binary_from_url(csv_lines[i].split(',')[2], './realreal-imgs/' + 'rr-' + str(i).zfill(5) + '.jpg')
        time.sleep(0.1)
