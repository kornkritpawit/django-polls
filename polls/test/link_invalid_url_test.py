from selenium import webdriver
import requests


def get_links(url):
    """Find all links on page at the given url.
       Return a list of all link addresses, as strings.
    """
    from webdriver_manager.chrome import ChromeDriverManager

    links = []
    browser = webdriver.Chrome(executable_path='/Users/sk/Desktop/chromedriver')
    browser.get(url)
    elements = browser.find_elements_by_tag_name("a")
    for a in elements:
        links.append(a.get_attribute('href'))
    browser.close()
    return links

def invalid_urls(urllist):
    invalid_list = []
    for link in urllist:
        r = requests.head(link)
        if r.status_code == 404:
            invalid_list.append(link)
    return invalid_list     


if __name__ == "__main__":
    hreflist = get_links("https://cpske.github.io/ISP/")
    for href in hreflist:
        print("Valid: " + href)
    invalid_url = invalid_urls(hreflist)        
    for invalid in invalid_url:
        print("Broken: " + invalid)
