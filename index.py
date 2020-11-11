"""
Author: Ryan Aquino
Description: Scrape lazada.com products
"""
from bs4 import BeautifulSoup
from selenium import webdriver


def selenium_html_scraper(url) -> str:
    """
    Returns the html source code of the url

    :param url: source url
    :return: html page source code
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = True

    chrome_driver = webdriver.Chrome(options=chrome_options)
    chrome_driver.get(url)
    html_source = chrome_driver.page_source

    chrome_driver.quit()
    return html_source


def scrape_product_item(product) -> dict:
    """
    Scrape a product details

    :param product:
    :return: dictionary of product name and price
    """
    product = product.findChildren("a", recursive=True)[0]
    product_url = product.get("href")

    product_html_source = selenium_html_scraper(f"https:{product_url}")
    soup = BeautifulSoup(product_html_source, "html.parser")

    title = soup.find("div", {"class": "pdp-product-title"}).text
    price = soup.find("div", {"class": "pdp-product-price"}).text
    price = f"₱{price.split('₱')[1]}"

    description_items = soup.find("div", {"class": "pdp-product-desc"}).findChildren(
        "li", recursive=True
    )
    description = ""

    for description_item in description_items:
        description += f"{description_item.text} \n"

    product_details = {"name": title, "description": description, "price": price}

    return product_details


def save_to_db(item):
    """
    Save product to database

    :param item: product item
    :return: None
    """
    pass


def category_scraper(html):
    """
    Extracts the items in the html source of a product category

    :param html: html page source code
    :return: None
    """
    soup = BeautifulSoup(html, "html.parser")
    products = soup.find_all(attrs={"data-qa-locator": "product-item"})

    for product in products:
        product_details = scrape_product_item(product)
        print(product_details)


if __name__ == "__main__":
    urls = [
        "https://www.lazada.com.ph/shop-mobiles/",
        "https://www.lazada.com.ph/shop-laptops/",
        "https://www.lazada.com.ph/shop-desktop-computers/",
    ]

    for url in urls:
        source = selenium_html_scraper(url)
        category_scraper(source)
