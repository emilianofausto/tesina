# -*- coding: utf-8 -*-

from hyper import HTTP20Connection
import time

index = 1
msg = 'tesina'
url = '127.0.0.1:8888'

connection = HTTP20Connection(url)
connection.connect()
connection.request('GET','/')

for letter in msg:
    streamID = index * 1000 + ord(letter)
    print 'Letter: %c (%d) - StreamID = %d' % (letter, ord(letter), streamID)
    index += 1
    connection.next_stream_id = streamID
    print 'Set connection.next_stream_id %d' % connection.next_stream_id
    connection.request('GET', '/')
    time.sleep(5)

connection.close()

print 'Sent message: %s to server' % msg

