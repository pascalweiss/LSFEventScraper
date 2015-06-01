__author__ = 'pascal'

from datetime import datetime

from bs4 import BeautifulSoup

from LSFEvent import LSFEvent
from LSFTextUtils import LSFTextUtils


class LSFEventParser:

    def __init__(self, html):
        self.dom = BeautifulSoup(html, from_encoding='utf-8')

    def extract_events(self):
        events = []
        date_str = self.extract_date()
        rows = self.extract_rows()
        row_count = 0
        for row in rows:
            event = LSFEventParser.convert_html_row(row, date_str)
            events.append(event)
            # try:
            #     event = LSFEventParser.convert_html_row(row, date_str)
            #     events.append(event)
            # except:
            #     failure_string = 'Failure on ' + date_str + ' at row ' + str(row_count)
            #     print(failure_string)
            #     LSFLogging.log_failure(failure_string)

            row_count += 1
        return events

    def extract_date(self):
        date_tag = self.dom.find('td', 'hd_darkgreen')
        return date_tag.text[29:39]

    def extract_rows(self):
        inside = self.dom.find('table', 'inside')
        tr = inside.find_all('tr')
        return tr[7:len(tr)-1]

    # @staticmethod
    # def tag_is_event(tag):
    #     if tag == True

    @staticmethod
    def convert_html_row(row, date_str=''):
        event = LSFEvent()
        td_tags = row.find_all('td')
        if len(td_tags) != 0:
            campus_and_building = LSFTextUtils.split_string_at_nth_space(td_tags[4].text, 1)
            begin_str = LSFTextUtils.correct_time_string(LSFTextUtils.remove_spaces(td_tags[0].text))
            end_str = LSFTextUtils.correct_time_string(td_tags[1].text)
            event.begin = datetime.strptime(date_str + ' ' + begin_str, '%d.%m.%Y %H:%M')
            event.end = datetime.strptime(date_str + ' ' + end_str, '%d.%m.%Y %H:%M')
            event.id = td_tags[2].text
            event.title = LSFTextUtils.remove_new_line_and_tab(td_tags[3].text)
            event.event_link = td_tags[3].find('a')['href']
            event.campus = LSFTextUtils.remove_spaces_at_end(campus_and_building[0])
            event.building = LSFTextUtils.rename_TGS(campus_and_building[1])
            event.room = LSFTextUtils.remove_new_line_and_tab(LSFTextUtils.split_string_at_last_space(td_tags[5].text)[1])
            event.room_link = td_tags[5].find('a')['href']
            event.student_group = LSFTextUtils.remove_spaces_at_beginning(td_tags[6].text)
            event.lecturer = LSFTextUtils.remove_spaces_at_beginning(td_tags[7].text)
        return event






