__author__ = 'pascal'

from urllib import urlopen
import time
from threading import Thread
from threading import active_count
from glob import glob


class LSFFetcher:
    overview_url = ""
    event_urls = []
    simultaneous_threads = 1

    def add_overview_url(self, overview_url):
        self.overview_url = overview_url

    def add_event_urls(self, event_urls):
        for url in event_urls:
            if url not in self.event_urls:
                self.event_urls.append(url)
        pass

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

    def fetch_local_sites(self, callback):
        html = ''
        files = glob('data/*.html')
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
        event_overview = self.fetch_url(self.overview_url)
        callback(event_overview)

    def fetch_event_sites(self, callback):
        threads = []
        for event_url in self.event_urls:
            thread = Thread(target=self.fetch_event_site, args=(event_url, callback))
            threads.append(thread)

        while threads != []:
            aux_threads = []
            for i in range(self.simultaneous_threads):
                try:
                    aux_threads.append(threads.pop())
                except:
                    print("WAT")
            for thread in aux_threads:
                thread.start()
            print('active threads: ' + str(active_count()))
            for thread in aux_threads:
                thread.join()

    def fetch_event_site(self, event_url, callback):
        event_site = self.fetch_url(event_url)
        callback(event_site)
