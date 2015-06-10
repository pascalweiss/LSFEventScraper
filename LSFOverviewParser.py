__author__ = 'pascal'

from LSFEventType import LSFEventType
from bs4 import BeautifulSoup

class LSFOverviewParser:

    @staticmethod
    def extract_links(html, event_type=LSFEventType.normal_event):
        soup = BeautifulSoup(html)
        a_tags = soup.find_all('a', 'klein')
        hrefs = []
        for a_tag in a_tags:
            hrefs.append(a_tag['href'])
        return LSFOverviewParser.create_urls_from_fetched_hrefs(hrefs, event_type)

    @staticmethod
    def create_urls_from_fetched_hrefs(hrefs, event_type=LSFEventType.normal_event):
        urls = []
        if event_type is LSFEventType.normal_event:
            type = str(0)
        else:
            type = str(1)
        for href in hrefs:
            date_str = href[:29]
            coockie_str = href[:30]
            url = 'https://lsf.htw-berlin.de/qisserver/rds?state=currentLectures&type=' + type + '&next=CurrentLectures.vm&nextdir=ressourcenManager' + date_str + '&asi='
            urls.append(url)
        return urls
