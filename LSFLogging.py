__author__ = 'pascal'

import time


class LSFLogging:

    @staticmethod
    def log_event(event, file = 'log.txt'):
        with open(file, 'a') as f:
            f.write(LSFLogging.event_to_string(event).encode('utf8') + '\n')

    @staticmethod
    def event_to_string(event):
        begin = ''
        end = ''
        if event.begin != None:
            begin = event.begin.strftime('%H:%M - %d.%m.%Y')
        if event.end != None:
            end = event.end.strftime('%H:%M - %d.%m.%Y')


        str = 'crawled on: ' + time.strftime('%c') + '\n'
        str += '====================================\n'
        str += 'title:      ' + event.title + '\n'
        str += 'begin:      ' + begin + '\n'
        str += 'end:        ' + end + '\n'
        str += 'campus:     ' + event.campus + '\n'
        str += 'building:   ' + event.building + '\n'
        str += 'room:       ' + event.room + '\n'
        str += 'group:      ' + event.student_group + '\n'
        str += 'lecturer:   ' + event.lecturer + '\n'
        str += 'event_link: ' + event.event_link + '\n'
        str += 'room_link:  ' + event.room_link + '\n'
        str += '\n'
        return str

    @staticmethod
    def log_failure(failure_string, file='log_failure.txt'):
        with open(file , 'a') as f:
            f.write(failure_string + '\n')