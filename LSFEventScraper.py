

__author__ = 'pascal'

from LSFFetcher import LSFFetcher
from LSFOverviewParser import LSFOverviewParser
from LSFEventParser import LSFEventParser
from LSFEventDBAccess_PSQL import LSFEventDBAccess
from LSFLogging import LSFLogging
from LSFEventType import LSFEventType

class LSFEventScraper:
    _events_normal = []
    _events_cancelled = []
    _event_type = LSFEventType.normal_event
    _overview_url = "https://lsf.htw-berlin.de/qisserver/rds?state=hiscalendar&type=0&asi="

    def set_to_cancelled_events(self):
        self._event_type = LSFEventType.cancelled_event

    def set_to_normal_event(self):
        self._event_type = LSFEventType.normal_event

    def __init__(self, event_type=LSFEventType.normal_event, logging=False):
        self.fetcher = LSFFetcher()
        self._event_type = event_type
        self.db_access = LSFEventDBAccess()
        self._logging = logging

    def _fetch_sites(self):
        self.fetcher.add_overview_url(self._overview_url)
        self.fetcher.fetch_event_overview(self._receive_event_overview)

    def crawl_events_and_save_to_disk(self):
        self._fetch_sites()
        self.fetcher.fetch_event_sites(self._save_to_disk)

    def crawl_events(self):
        self._fetch_sites()
        self.fetcher.fetch_event_sites(self._receive_event_data)

    def crawl_local_sites(self):
        self.fetcher.fetch_local_sites(self._receive_event_data, event_type=self._event_type)

    def save_events_to_db(self):
        if self._event_type is LSFEventType.normal_event:
            self.db_access.add_events(self._events_normal)
        else:
            self.db_access.add_cancel_notes(self._events_cancelled)

#            _ _ _                _
#   ___ __ _| | | |__   __ _  ___| | _____
#  / __/ _` | | | '_ \ / _` |/ __| |/ / __|
# | (_| (_| | | | |_) | (_| | (__|   <\__ \
#  \___\__,_|_|_|_.__/ \__,_|\___|_|\_\___/

    def _save_to_disk(self, html):
        parser = LSFEventParser(html, event_type=self._event_type)
        date = parser.extract_date()
        if self._event_type is LSFEventType.normal_event:
            folder = 'data_events/'
        else:
            folder = 'data_cancels/'
        with open(folder + date + '.html', 'w') as f:
            f.write(html)

    def _receive_event_overview(self, overview):
        links = LSFOverviewParser.extract_links(overview)
        self.fetcher.add_event_urls(links)

    def _receive_event_data(self, html):
        parser = LSFEventParser(html, event_type=self._event_type)
        new_events = parser.extract_events()
        if self._event_type == LSFEventType.normal_event:
            self._events_normal += new_events
        else:
            self._events_cancelled += new_events
        if self._logging:
            for event in new_events:
                LSFLogging.log_event(event)
