from LSFEventType import LSFEventType

__author__ = 'pascal'

from urllib import urlopen
import time
from threading import Thread
from threading import active_count
from glob import glob


class LSFFetcher:
    _overview_url = ''
    _event_urls = []
    simultaneous_threads = 5

    def add_overview_url(self, overview_url):
        self._overview_url = overview_url

    def add_event_urls(self, event_urls):
        for url in event_urls:
            if url not in self._event_urls:
                self._event_urls.append(url)

    def fetch_url(self, url):
        result = ''
        while True:
            try:
                result = urlopen(url).read()
                break
            except Exception as e:
                print('Problem with Internet Connection')
                time.sleep(2)
        return result

    def fetch_local_sites(self, callback, event_type=LSFEventType.normal_event):
        html = ''
        if event_type is LSFEventType.normal_event:
            files = glob('data_events/*.html')
        else:
            files = glob('data_cancels/*.html')
        for file in files:
            with open(file, 'r') as f:
                html = f.read()
            callback(html)

    def fetch_local_site(self, callback):
        html = ''
        with open('data_example.html', 'r') as f:
            html = f.read()
        callback(html)

    def fetch_event_overview(self, callback):
        event_overview = self.fetch_url(self._overview_url)
        callback(event_overview)

    def fetch_event_sites(self, callback):
        threads = []
        for event_url in self._event_urls:
            thread = Thread(target=self.fetch_event_site, args=(event_url, callback))
            threads.append(thread)

        while threads != []:
            aux_threads = []
            for i in range(self.simultaneous_threads):
                try:
                    aux_threads.append(threads.pop())
                except Exception as e:
                    print(e)
            for thread in aux_threads:
                thread.start()
            print('Fetching: ' + str(len(threads)) + ' sites left.' + ' Active fetching threads: ' + str(self.simultaneous_threads))
            for thread in aux_threads:
                thread.join()

    def fetch_event_site(self, event_url, callback):
        event_site = self.fetch_url(event_url)
        callback(event_site)
