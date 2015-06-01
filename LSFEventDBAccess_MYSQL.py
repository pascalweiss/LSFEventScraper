__author__ = 'pascal'

import mysql.connector
from datetime import datetime
import json

class LSFEventDBAccess:
    def __init__(self):
        credentials = json.load(open('db_credentials_MYSQL.json', 'r'))

        self.cnx = mysql.connector.connect(**credentials)

    def add_events(self, events):
        cursor = self.cnx.cursor()
        chunks = self.events_to_chunks(events,1000)
        for chunk in chunks:
            add_event = ('INSERT INTO events '
                         '(id, begin, end, title, event_link, campus, building, room, room_link, student_group, lecturer)'
                         'VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s)')
            success = False
            while not success:
                try:
                    cursor.executemany(add_event, chunk)
                    success = True
                except Exception as e:
                    print(e)
            self.cnx.commit()


    def add_event(self, event):
        cursor = self.cnx.cursor()
        add_event = ('INSERT INTO events '
                     '(id, begin, end, title, event_link, campus, building, room, room_link, student_group, lecturer)'
                     'VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s)')
        event_data = (event.id, datetime.now(), datetime.now(), event.title, event.event_link, event.campus, event.building, event.room, event.room_link, event.student_group, event.lecturer)
        cursor.execute(add_event, event_data)
        self.cnx.commit()

    # doesn't work right now
    # =======================
    # def initialize_db(self):
    #     cursor = self.cnx.cursor()
    #     query = ''
    #     with open('RoomDBInit_MYSQL.db', 'r') as f:
    #         query = f.read()
    #     cursor.execute(query, multi = True)
    #     self.cnx.commit()

    # resets all data + resets auto_increment (although it isn't used here)

    def events_to_chunks(self, events, size):
        chunks = []
        arr = []
        s = size
        for i in range(len(events)):
            event = events[i]
            arr.append([event.id, event.begin, event.end, event.title, event.event_link, event.campus, event.building, event.room, event.room_link,event.student_group,event.lecturer])
            if s == 1:
                chunks.append(arr)
                arr = []
                s = size
            else:
                s -= 1
        chunks.append(arr)
        return chunks

    def reset(self):
        cursor = self.cnx.cursor()
        cursor.execute('TRUNCATE events')
        self.cnx.commit()

    def close_connection(self):
        self.cnx.close()
