__author__ = 'pascal'

from LSFEventScraper import LSFEventScraper

controller = LSFEventScraper()
# controller.crawl_events()
controller.crawl_local_sites()
controller.db_access.reset()
controller.save_events_to_db()