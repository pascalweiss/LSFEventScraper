__author__ = 'pascal'

from bs4 import BeautifulSoup

class LSFOverviewParser:

    @staticmethod
    def extract_links(html):
        soup = BeautifulSoup(html)
        a_tags = soup.find_all('a', 'klein')
        hrefs = []
        for a_tag in a_tags:
            hrefs.append(a_tag['href'])
        return LSFOverviewParser.create_urls_from_fetched_hrefs(hrefs)

    @staticmethod
    def create_urls_from_fetched_hrefs(hrefs):
        urls = []
        for href in hrefs:
            date_str = href[:29]
            coockie_str = href[:30]
            url = 'https://lsf.htw-berlin.de/qisserver/rds?state=currentLectures&type=0&next=CurrentLectures.vm&nextdir=ressourcenManager' + date_str + '&asi='
            urls.append(url)
        return urls
