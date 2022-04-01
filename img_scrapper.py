import urllib.request

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time

COLLECTION_LINK = "https://unsplash.com/images/nature/fall"
MIN_IMAGES = 1000
DOWNLOAD_HIGH_QUALITY = False
FIRST_ID = 339

# Place driver in CWD (this setup uses Firefox)
# At this you can change web browser, 
# but install browser and download driver first
from selenium.webdriver.common.by import By
browser = webdriver.Firefox(executable_path='./geckodriver')
# Maximize window just for fun
browser.maximize_window()

def load_page(url=None):
    global browser
    # Add https part to url if needed
    if not 'http://' in url and not 'https://' in url : url = 'https://' + url
    browser.get(url)
    print("Loaded page", url)


# Example function to refresh currently focused tab
def perform_refresh():
    global browser
    browser.refresh()
    print("Refreshed page")


def move_to_element(element):
    ActionChains(browser).move_to_element(element).perform()


def find_image_class_name():
    all_imgs = browser.find_elements(By.XPATH, "//img")
    for img in all_imgs:
        img_src = img.get_attribute("src")
        if "1000&q=80" in img_src:
            return img.get_attribute("class")


load_page(COLLECTION_LINK)
perform_refresh()

more_btn = browser.find_element(By.XPATH, "//button[text()=\"Load more photos\"]")

browser.execute_script("arguments[0].click();", more_btn)


print("Starting to scrap...")
if DOWNLOAD_HIGH_QUALITY:
    # Use download buttons (high quality but slow)
    downloads = []
    while len(downloads) < MIN_IMAGES:
        browser.execute_script("window.scrollBy(0, 1000);")
        downloads = browser.find_elements(By.XPATH, "//a[@title=\"Download photo\"]")
        time.sleep(1)
        print("Currently found", len(downloads), "download buttons")

    for i in range(len(downloads)):
        print("Downloading", str(i+1) + "/" + str(len(downloads)))
        download_url = downloads[i].get_attribute("href")
        urllib.request.urlretrieve(download_url, "out/image_" + str(FIRST_ID + i) + ".jpg")
else:
    # Use already loaded images (fast but low quality)
    class_name = find_image_class_name()
    imgs = []
    while len(imgs) < MIN_IMAGES:
        browser.execute_script("window.scrollBy(0, 1000);")
        imgs = browser.find_elements(By.XPATH, "//img[@class=\"" + class_name + "\"]")
        time.sleep(1)
        print("Currently found", len(imgs), "loaded images")

    for i in range(len(imgs)):
        print("Downloading", str(i+1) + "/" + str(len(imgs)))
        download_url = imgs[i].get_attribute("src")
        urllib.request.urlretrieve(download_url, "out/image_low_" + str(FIRST_ID + i) + ".jpg")


if __name__ == '__main__':
    pass