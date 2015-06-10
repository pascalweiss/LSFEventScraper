__author__ = 'pascal'

import psycopg2
from datetime import datetime
import json

class LSFEventDBAccess:
    chunk_size = 500

    def __init__(self):
        credentials = json.load(open('db_credentials_PSQL.json', 'r'))
        self.cnx = psycopg2.connect(**credentials)

    def add_events_old(self, events):
        cursor = self.cnx.cursor()
        chunks = self.events_to_insert_chunks(events, self.chunk_size)
        for chunk in chunks:
            add_event = ('INSERT INTO events '
                         '(id, begin, finish, title, event_link, campus, building, room, room_link, student_group, lecturer)'
                         'VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s)')
            success = False
            while not success:
                try:
                    cursor.executemany(add_event, chunk)
                    success = True
                except Exception as e:
                    print(e)
            self.cnx.commit()

    def add_events(self, events_normal):
        cursor = self.cnx.cursor()
        chunks = self.events_to_insert_chunks(events_normal, self.chunk_size)
        aux = len(chunks)
        for chunk in chunks:
            if len(chunk) is not 0:
                # http://stackoverflow.com/questions/8134602/psycopg2-insert-multiple-rows-with-one-query
                value_str = ','.join(cursor.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", x) for x in chunk)
                add_event = 'INSERT INTO events VALUES '
                success = False
                while not success:
                    try:
                        cursor.execute(add_event + value_str)
                        success = True
                    except Exception as e:
                        print(e)
                aux -= 1
                print('Inserting in DB: ' + str(aux) + ' chunks left (chunk_size = ' + str(self.chunk_size) + ' events)')
                self.cnx.commit()

    def add_cancel_notes(self, events_cancel):
        cursor = self.cnx.cursor()
        chunks = self.events_to_update_chunks(events_cancel,self.chunk_size)
        for chunk in chunks:
            update_query = ('UPDATE events '
                         'SET cancel_note=%s '
                         'WHERE id=%s AND begin=%s AND finish=%s AND title=%s')
            success = False
            while not success:
                try:
                    cursor.executemany(update_query, chunk)
                    success = True
                except Exception as e:
                    print(e)
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

    def events_to_update_chunks(self, events, size):
        chunks = []
        arr = []
        s = size
        for i in range(len(events)):
            event = events[i]
            arr.append([event.cancel_note, event.id, event.begin, event.end, event.title])
            if s == 1:
                chunks.append(arr)
                arr = []
                s = size
            else:
                s -= 1
        chunks.append(arr)
        return chunks

    def events_to_insert_chunks(self, events, size):
        chunks = []
        arr = []
        s = size
        for i in range(len(events)):
            event = events[i]
            arr.append([event.id, event.begin, event.end, event.title, event.event_link, event.campus, event.building, event.room, event.room_link,event.student_group,event.lecturer, event.cancel_note])
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
