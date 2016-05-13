#!/usr/bin/env python
import requests
import string
from uuid import uuid4
from time import time
from pprint import pprint
from bson.json_util import loads, dumps
import threading
import pika
import socket
from sys import stdin, stdout, exit
from pymongo import MongoClient

con = MongoClient()
col = con.socket

# Socket client host and port
host = "riboflav.in"
port = 6667
mode = "client"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Start consuming the message queue for things to do
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='stream', type='fanout')

def stop_socket() :
	sock.exit()

def start_socket() :
	readbuffer = ''
	sock.connect(("riboflav.in", 6667))
	while True :
		readbuffer = readbuffer + sock.recv(1024)
		temp = string.split(readbuffer, "\n")
		readbuffer = temp.pop()
		for line in temp :
			body = {
				'uuid' : str(uuid4()),
				'raw'  : line,
				'args' : line.split(),
				'host' : host,
				'port' : port,
				'time' : time(),
				'event': "socket"
			}
			channel.basic_publish(exchange='stream', routing_key='', body=dumps(body))

def mq_callback(ch, method, properties, body) :

	body = loads(body)
	args = body.get("args")
	host = body.get("host")
	port = body.get("host")
	time = body.get("time")
	uuid = body.get("uuid")
	raw = body.get("raw")
	event = body.get("event")
	col.log.insert(body)
        result = None
        pprint(body)

        for rule in col.rules.find() :
            title = rule.get("title")
            condition = rule.get("condition")
            actions = rule.get("actions")
            execute = rule.get('exec')

            for k,v in condition.iteritems() :

                try :
                    test = args[int(k)] == v
                except :
                    pass

                if test :

                    print "Executing %s" % title
                    # See if there's an exec block
                    if execute :
                        typeof = execute.get('type')
                        valof = execute.get('value')
                        print "%s:%s" % (typeof, valof)

                        if typeof == 'JSON' :
                            try :
                                result = requests.post(valof, json=dumps(body)).json().get('result')
                                args.append(result)
                            except :
                                pass

                    for action in actions :
                        # this stupid thing just replaces vars in the string
                        argdict = dict(k for k in enumerate(args))
                        argdict.update({'result': result})
                        final = dict([(str(k), v) for k, v in argdict.items()])
                        msg = action % final # {str(k) : v for k, v in enumerate(args)}
                        print "MESSAGE : %s" % msg
                        for ms in msg.split("\n") :
                            sock.send(ms+"\r\n")
                
def init_mq() :
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='stream', queue=queue_name)
    channel.basic_consume(mq_callback, queue=queue_name, no_ack=True)
    channel.start_consuming()


# Start rabbitmq thread as well as socket client
def start() :

	mthread = threading.Thread(target=init_mq)
	mthread.daemon = True
	mthread.start()

	# Socket client will write to amq buffer
	start_socket()
	

if __name__ == "__main__" :
	try :
		start()
	except KeyboardInterrupt :
		exit(1)
