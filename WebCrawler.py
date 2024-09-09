from urllib.parse import urljoin, urlparse
import requests
import subprocess
from bs4 import BeautifulSoup

unique_urls = set()


def verify_URL(URL):
    parsed_URL = urlparse(URL)
    return parsed_URL.scheme in ['http', 'https'] and bool(parsed_URL.netloc) 

def crawl_website(base_URL): # Function to extract links out of the page
    try:
        response = requests.get(base_URL)
    except requests.RequestException as e:
        print(f"Request failed for {base_URL} : {e}")
        return


    if response.status_code == 200 or response.status_code == 403:
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a')
        extracted_urls = []


    # extract the links
        for link in links:
            href = link.get('href')
            if href and href != '':
                extracted_urls.append(href)
        
        if not extracted_urls:
            print('Nothing found!')
            return

    # filter out the unique links
        for url in extracted_urls:
            if url not in unique_urls:
                unique_urls.add(url)
                new_url = urljoin(base_URL, url)
                crawl_website(new_url)
    
    # filter out the live links
        try:
            subprocess.run(['python3', 'LinkProber.py'] + list(unique_urls), check=True)
        except subprocess.CalledProcessError as e:
            print(f'Error {e}\n')


if __name__ == '__main__':
    URL = input('Enter the absolute URL: ')
    if (verify_URL(URL)):
        crawl_website(URL)
    else:
        print('Usage: python3 http://example.com OR python3 https://example.com')