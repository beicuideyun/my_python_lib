# -*- coding: utf-8 -*-

"""
rabbit mq received related functions
Created on 2019-03-12
@author: beicuideyun
"""

from rabbit import Rabbit
import time
import sys
import pika


class Rabbit_receive(object):
    def __init__(self):
        self.__rabbit = Rabbit(host="localhost")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__rabbit.close()

    def simple_mode(self, callback=None, queue_name="simple", durable=False):
        self.__rabbit.declare_queue(queue_name=queue_name, durable=durable)
        receive_callback = callback if callback is not None else self.on_simple_mode_callback
        self.__rabbit.consume(receive_callback, queue_name=queue_name, no_ack=True)
        self.__rabbit.start()

    def on_simple_mode_callback(self, ch, method, properties, body):
        print(" [x] Received %r" % body)

    def fanout_mode(self, callback=None, exchange_name="logs"):
        self.__rabbit.declare_exchange(exchange_name=exchange_name)
        result = self.__rabbit.declare_queue_exclusive()
        queue_name = result.method.queue
        self.__rabbit.bind(exchange=exchange_name, queue_name=queue_name)
        receive_callback = callback if callback is not None else self.on_simple_mode_callback
        self.__rabbit.consume(receive_callback, queue_name=queue_name, no_ack=True)
        self.__rabbit.start()

    def direct_mode(self, callback=None, exchange_name="direct_logs", binding_keys=[]):
        self.__rabbit.declare_exchange(exchange_name=exchange_name, exchange_type="direct")
        result = self.__rabbit.declare_queue_exclusive()
        queue_name = result.method.queue
        for binding_key in binding_keys:
            self.__rabbit.bind(exchange=exchange_name, queue_name=queue_name, routing_key=binding_key)
        receive_callback = callback if callback is not None else self.on_simple_mode_callback
        self.__rabbit.consume(receive_callback, queue_name=queue_name, no_ack=True)
        self.__rabbit.start()

    def rpc_mode(self, callback=None, queue_name="rpc_queue"):
        self.__rabbit.declare_queue(queue_name=queue_name)
        self.__rabbit.qos()
        receive_callback = callback if callback is not None else self.on_rpc_mode_callback
        self.__rabbit.consume(receive_callback, queue_name=queue_name)
        self.__rabbit.start()

    def on_rpc_mode_callback(self, ch, method, props, body):
        print(" [.] received one msg (%s)" % body)
        response = body
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id=props.correlation_id),
                         body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print(" [x] done")


def callback_sendack(ch, method, properties, body):   # no_ack=False
    print(" [x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print(" [x] done")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def callback_direct(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))


if __name__ == '__main__':
    with Rabbit_receive() as recv:
        recv.rpc_mode()
    #severities = sys.argv[1:]
    #if not severities:
    #    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    #    sys.exit(1)
    #with Rabbit_receive() as recv:
    #    recv.direct_mode(callback=callback_direct, exchange_name="direct_logs", binding_keys=severities)

    #with Rabbit_receive() as recv:
    #    recv.fanout_mode(exchange_name="logs")

    #with Rabbit_receive() as recv:
    #    recv.simple_mode(callback_sendack, queue_name="task_queue", durable=True)

    #with Rabbit_receive() as recv:
    #    recv.simple_mode(callback=callback)

    ## simple mode
    #with Rabbit_receive() as recv:
    #    recv.simple_mode()