__author__ = 'pascal'

from LSFFetcher import LSFFetcher
from LSFOverviewParser import LSFOverviewParser
from LSFEventParser import LSFEventParser
from LSFEventDBAccess_PSQL import LSFEventDBAccess
from LSFLogging import LSFLogging


class LSFEventScraper:
    events = []
    LSFEventSite = "https://lsf.htw-berlin.de/qisserver/rds?state=hiscalendar&type=0&asi="

    def __init__(self):
        self.fetcher = LSFFetcher()
        self.db_access = LSFEventDBAccess()

    def crawl_events_and_save_to_disk(self):
        self.fetcher.add_overview_url(self.LSFEventSite)
        self.fetcher.fetch_event_overview(self.receive_event_overview)
        self.fetcher.fetch_event_sites(self.save_to_disk)


    def crawl_url(self, url):
        self.fetcher.fetch_event_site(url, self.receive_event_data)

    def crawl_events(self):
        self.fetcher.add_overview_url(self.LSFEventSite)
        self.fetcher.fetch_event_overview(self.receive_event_overview)
        self.fetcher.fetch_event_sites(self.receive_event_data)

    def crawl_local_sites(self):
        self.fetcher.fetch_local_sites(self.receive_event_data)

    def save_events_to_db(self):
        self.db_access.add_events(self.events)
        # for event in self.events:
        #     self.db_access.add_event(event)

#            _ _ _                _
#   ___ __ _| | | |__   __ _  ___| | _____
#  / __/ _` | | | '_ \ / _` |/ __| |/ / __|
# | (_| (_| | | | |_) | (_| | (__|   <\__ \
#  \___\__,_|_|_|_.__/ \__,_|\___|_|\_\___/

    def save_to_disk(self, html):
        parser = LSFEventParser(html)
        date = parser.extract_date()
        with open('data/' + date + '.html', 'w') as f:
            f.write(html)

    def receive_event_overview(self, overview):
        links = LSFOverviewParser.extract_links(overview)
        self.fetcher.add_event_urls(links)

    def receive_event_data(self, html):
        parser = LSFEventParser(html)
        new_events = parser.extract_events()
        self.events += new_events
        for event in new_events:
            LSFLogging.log_event(event)
