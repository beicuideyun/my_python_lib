# -*- coding: utf-8 -*-

"""
rabbit mq send related functions
Created on 2019-03-12
@author: beicuideyun
"""

from rabbit import Rabbit
import sys
import uuid
import pika

class Rabbit_send(object):
    def __init__(self):
        self.__rabbit = Rabbit(host="localhost")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__rabbit.close()

    def simple_mode(self, body, queue_name="simple", is_msg_durable=False):
        self.__rabbit.declare_queue(queue_name=queue_name, durable=is_msg_durable) # 队列持久化
        self.__rabbit.publish(body=str(body), exchange_name="", routing_key=queue_name, is_msg_durable=is_msg_durable) #消息持久化

    def fanout_mode(self, body, exchange_name):
        self.__rabbit.declare_exchange(exchange_name=exchange_name, exchange_type="fanout")
        self.__rabbit.publish(body=str(body), routing_key="", exchange_name=exchange_name)

    def direct_mode(self, body, exchange_name, routing_key):
        self.__rabbit.declare_exchange(exchange_name=exchange_name, exchange_type="direct")
        self.__rabbit.publish(body=str(body), exchange_name=exchange_name,routing_key=routing_key)

    def rpc_mode(self, callback=None):
        result = self.__rabbit.declare_queue_exclusive()
        self.callback_queue = result.method.queue
        receive_callback = callback if callback is not None else self.on_rpc_response
        self.__rabbit.consume(receive_callback, queue_name=self.callback_queue, no_ack=True)

    def on_rpc_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.__rabbit.response = body

    def rpc_call(self, body, routing_key="rpc_queue"):
        self.corr_id = str(uuid.uuid4())
        return self.__rabbit.call(self.corr_id, self.callback_queue, body, routing_key=routing_key)


if __name__ == '__main__':
    with Rabbit_send() as send:
        send.rpc_mode()
        print(" [x] Requesting (30)")
        response = send.rpc_call(30)
        print(" [.] Got %r" % response)

    #with Rabbit_send() as send:
    #    severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
    #    message = ' '.join(sys.argv[2:]) or 'Hello World!'
    #    send.direct_mode(message, "direct_logs", severity)

    ## fanout mode
    #message = ''.join(sys.argv[1:]) or "info: Hello World!"
    #with Rabbit_send() as send:
    #    send.fanout_mode(message, exchange_name="logs")

    ## ack and taks queue
    #message = ' '.join(sys.argv[1:]) or "Hello World!"
    #with Rabbit_send() as send:
    #    send.simple_mode(message, queue_name="task_queue", is_msg_durable=True)

    ## work queue
    #message = '.'.join(sys.argv[1:]) or "Hello World!"
    #with Rabbit_send()as send:
    #    send.simple_mode(message)

    ## simple mode
    #with Rabbit_send() as send:
    #    send.simple_mode("Hello World!")
    #    #send.simple_mode({"hello": "world"})