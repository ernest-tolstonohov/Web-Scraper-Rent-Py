import undetected_chromedriver
from bs4 import BeautifulSoup
import time

# VERSION 1.0
# Main URL - Useful later for link building

MAIN_URl = "https://www.openrent.co.uk"

# URL - Search link for London
URL = "https://www.openrent.co.uk/properties-to-rent/london?term=London"

# Setting search
setting_search = {
    "&area=": "10",
    "&prices_min=": "100",
    "&prices_max=": "1000",
    "&bedrooms_min=": "1",
    "&bedrooms_max=": "1",
}

# Building our link
for y in setting_search.keys():
    URL += y + setting_search[y]
print(URL)

# Parser function


def parser():
    # Upload WebDriver Chrome
    driver = undetected_chromedriver.Chrome()

    # Go to the Link
    driver.get(URL)
    # Save HTML as page_source
    page_source = driver.page_source
    # Loading BeautifulSoup
    soup = BeautifulSoup(page_source, "html.parser")
    # Get text how many offers we have
    text = soup.find("span", class_="filter-info").get_text()
    number = ""
    # Search only numbers
    for x in text:
        if x.isdigit():
            number += str(x)
    # Create dictionary for offers
    information = {
        0: {
            "street": None,
            "MPM": None,
            "distance": None,
            "rate": None,
            "URL": None
        }
    }
    # We load the page on which our offers are located (only 19 offers per page)
    for i in range(10, int(number), 20):
        upload_url = URL + f"&viewingProperty={i}"
        driver.get(upload_url)
        # Sleep to fully load the page(if you have good internet connection you can reduce the number of waits
        time.sleep(10)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        # Print number of offers
        print(i)
        for k in range(i - 10, i + 10):
            # Try to get a text because it isn't always available
            try:
                street = soup.find("a", sortorder=str(k)).find("span", class_="banda pt listing-title").get_text()
                MPM = soup.find("a", sortorder=str(k)).find("div", class_="pim pl-title").get_text()
                distance = soup.find("a", sortorder=str(k)).find("div", class_="ltc pl-title",
                                                                 title="Click to highlight on map").get_text()
                rate = None
                url_flat = MAIN_URl + soup.find("a", sortorder=str(k)).get("href")
                # Filling dictionary
                information[k] = {
                    "street": street,
                    "MPM": MPM,
                    "distance": distance,
                    "rate": rate,
                    "URL": url_flat
                }
            # if we have a problems, print errors
            except Exception as ex:
                print(ex)

    driver.close()
    driver.quit()


if __name__ == '__main__':
    parser()
