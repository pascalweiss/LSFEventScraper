from LSFEventScraper import LSFEventScraper
from LSFEventType import LSFEventType

__author__ = 'pascal'


scraper = LSFEventScraper(event_type=LSFEventType.normal_event, logging=False)

# FIRST SCENARIO
#===============

# - Fetches all events from HTW-Berlin.de and stores them to memory.
scraper.scrape_events()

# - Sends a TRUNCATE command to the database, to delete all current rows.
scraper.db_access.reset()

# - Sends saves all events to the database.
scraper.save_events_to_db()

# SECOND SCENARIO
#================

# - Fetches all day-overviews and stores them as html files to ./data_events/
# scraper.crawl_day_pages_and_save_to_disk()

# - ...Later... After you've fetched the pages, you can scrape and store the events later.

# - Scrapes all local sites and stores them to memory
#scraper.scrape_local_sites()
# - Sends a TRUNCATE command to the database, to delete all current rows.
#scraper.db_access.reset()
# - Sends saves all events to the database.
#scraper.save_events_to_db()
