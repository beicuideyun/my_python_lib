# -*- coding: utf-8 -*-

"""
rabbit mq basic functions
Created on 2019-03-12
@author: beicuideyun
"""

import pika


class Rabbit(object):
    def __init__(self, host="localhost"):
        self.__connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.__channel = self.__connection.channel()
        self.__response = None

    def declare_queue(self, queue_name='hello', durable=False):
        # durable=True queue durable
        self.__channel.queue_declare(queue=queue_name, durable=durable)

    def declare_queue_exclusive(self):
        return self.__channel.queue_declare(exclusive=True)

    def declare_exchange(self, exchange_name="logs", exchange_type="fanout"):
        self.__channel.exchange_declare(exchange=exchange_name,
                                        exchange_type=exchange_type)

    def bind(self, exchange, queue_name, routing_key=""):
        if routing_key == "":
            self.__channel.queue_bind(exchange=exchange,
                                      queue=queue_name)
        else:
            self.__channel.queue_bind(exchange=exchange,
                                      queue=queue_name,
                                      routing_key=routing_key)

    def publish(self, body, exchange_name='', routing_key='hello', is_msg_durable=False):
        if is_msg_durable is False:
            self.__channel.basic_publish(exchange=exchange_name,
                                         routing_key=routing_key,
                                         body=body)
        else:
            self.__channel.basic_publish(exchange=exchange_name,
                                         routing_key=routing_key,
                                         body=body,
                                         properties=pika.BasicProperties(
                                             delivery_mode=2,  # make message persistent
                                         ))
        print(" [x] Sent one msg! %s" % body)

    def qos(self):
        self.__channel.basic_qos(prefetch_count=1)

    def close(self):
        self.__connection.close()

    def consume(self, callback, queue_name='hello', no_ack=False):
        self.__channel.basic_consume(callback, queue=queue_name, no_ack=no_ack)

    def start(self):
        self.__channel.start_consuming()

    def call(self, correlation_id, callback_queue, body, routing_key="rpc_queue", exchange_name=""):
        self.response = None
        self.__channel.basic_publish(exchange=exchange_name,
                                     routing_key=routing_key,
                                     properties=pika.BasicProperties(
                                         reply_to=callback_queue,
                                         correlation_id=correlation_id,
                                     ),
                                     body=str(body))
        while self.response is None:
            self.__connection.process_data_events()
        return self.response