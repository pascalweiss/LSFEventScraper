from LSFEventScraper import LSFEventScraper
from LSFEventType import LSFEventType

__author__ = 'pascal'

controller = LSFEventScraper(event_type=LSFEventType.normal_event, logging=False)
controller.crawl_events()
# controller.crawl_local_sites()
controller.db_access.reset()
controller.save_events_to_db()

# controller.set_to_cancelled_events()
# controller.crawl_events_and_save_to_disk()
# controller.crawl_local_sites()

# controller.db_access.reset()
# controller.save_events_to_db()
