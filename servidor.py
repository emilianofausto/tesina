# -*- coding: utf-8 -*-

import socket
import os
import sys
import json
import h2.connection
import h2.events

from socket import error as SocketError
import errno

phrase_received = list()

"""
http://python-hyper.org/h2/en/latest/basic-usage.html#connections

Most H2Connection functions take a stream ID: they require you to actively tell the connection which one to use. In this case, as a simple server, we will never need to choose a stream ID ourselves: the client will always choose one for us. That means we will always be able to get the one we need off the events that fire.
"""


def send_response(conn, event):
    stream_id = event.stream_id
    if stream_id != 1:
        print stream_id
    response_data = json.dumps(dict(event.headers)).encode('utf-8')

    conn.send_headers(
        stream_id=stream_id,
        headers={
            ':status': '200',
            'server': 'basic-h2-server/1.0',
            'content-length': str(len(response_data)),
            'content-type': 'application/json',
        },
    )
    conn.send_data(
        stream_id=stream_id,
        data=response_data,
        end_stream=True
    )
    phrase_received.append(stream_id)

def imprimePhraseReceived(phrase):
    processedPhrase = "Phrase received: "
    i = 1
    for letra in phrase:
        pLetra = letra % ( i * 1000)
        if pLetra > 1:
            processedPhrase += chr(pLetra)

    print processedPhrase

def handle(sock):
    conn = h2.connection.H2Connection(client_side=False)
    conn.initiate_connection()
    sock.sendall(conn.data_to_send())

    try:

        while True:
            data = sock.recv(65535)
            if not data:
                h2.events.StreamReset
                break

            events = conn.receive_data(data)
            for event in events:
                if isinstance(event, h2.events.RequestReceived):
                    send_response(conn, event)

            data_to_send = conn.data_to_send()
            if data_to_send:
                sock.sendall(data_to_send)
    except SocketError as e:
        if e.errno != errno.ECONNRESET:
            raise
        else:
            imprimePhraseReceived(phrase_received)
            print "The client closed the connection"

sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('0.0.0.0', 8888))
sock.listen(5)

print "Listening on port 8888"

while True:
    handle(sock.accept()[0])
