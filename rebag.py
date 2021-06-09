import shutil

from selenium import webdriver
from bs4 import BeautifulSoup

import requests

import time


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


def get_and_save_rebag_image_links(driver, page_num, save_file, verbose=False):
    scrape_url = "https://shop.rebag.com/collections/all-bags?page=" + str(page_num) + "&_=pf&pf_st_availability_hidden" \
                                                                                   "=true&pf_t_categories=bc-filter" \
                                                                                   "-Bags"

    # Open page in test browser
    driver.get(scrape_url)

    # Superstitious additional wait
    driver.implicitly_wait(0.5)

    # Get source
    pg_src = driver.page_source

    # Parse source
    soup = BeautifulSoup(pg_src, 'html.parser')

    # Save bag links to file
    new_bags = []
    for div in soup.find_all("div", {"class": "plp-product"}):
        file_link = div.find("img")['src'].replace('260x260', '512x512')
        brand_and_name = div.find("div", {"class": "inner-focus"}).find("div", {"class": "product-caption"})
        brand = brand_and_name.find("div", {"class": "product-vendor"}).text.strip().replace(',', '')
        name = brand_and_name.find("div", {"class": "product-title"}).text.strip().replace(',', '')

        new_bags.append([brand, name, file_link])
    csv_append_save(new_bags, save_file)

    if verbose:
        print("Saved page " + str(page_num))

    return



def csv_append_save(sets, filename):
    """
    Non-destructive multipurpose data saver that appends to a file (creating it if need be)

    :param sets: Set of sets of data to append and save
    :param filename: Filname to append to
    """
    csvized_data = '\n'.join([','.join([str(v) for v in s]) for s in sets]) + '\n'
    f = open(filename, 'a')
    f.write(csvized_data)
    f.close()


if __name__ == '__main__':
    webdriver_path = 'insert-your-path'
    chromedriver = webdriver.Chrome(executable_path=webdriver_path)
    for pg in range(1, 297):
        get_and_save_rebag_image_links(chromedriver, pg, "baglinks.csv", verbose=True)

    f = open("baglinks.csv", 'r')
    contents = f.read()
    f.close()

    csv_lines = contents.split('\n')
    for i in range(12816, len(csv_lines)):
        # print(line.split(',')[2])
        save_binary_from_url(csv_lines[i].split(',')[2], './rebag-imgs/' + str(i).zfill(5) + '.jpg')
        time.sleep(0.1)

