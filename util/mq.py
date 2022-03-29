import json
from pprint import pprint

import pika

from util.escape import safe_json_decode


class RabbitMQConsumer(object):
    def __init__(self, host, queue, arguments=None):
        self.connection = pika.BlockingConnection(pika.URLParameters(host))
        self.queue = queue
        self.channel = self.connection.channel()
        # print(self.queue)
        self.channel.queue_declare(self.queue, durable=True, arguments=arguments)
        self.channel.basic_qos(prefetch_count=1)

    def begin_consume(self, callback):
        self.channel.basic_consume(on_message_callback=callback, queue=self.queue)
        self.channel.start_consuming()

    def close(self):
        pass


class RabbitMQProducer(object):
    def __init__(self, host, queue):
        self.host = host
        self.queue = queue

    def send_message(self, message, qn=0):
        connection = pika.BlockingConnection(pika.URLParameters(self.host))
        # creds_broker = pika.PlainCredentials("guest", "o2o")
        # connection = pika.BlockingConnection(pika.ConnectionParameters(self.host, credentials=creds_broker))

        channel = connection.channel()
        channel.queue_declare(queue=self.queue, durable=True)
        channel.basic_publish(exchange='', routing_key=self.queue, body=message,
                              properties=pika.BasicProperties(delivery_mode=2))
        connection.close()

    def send_priority_message(self, message, priority=10):
        connection = pika.BlockingConnection(pika.URLParameters(self.host))

        channel = connection.channel()
        arguments = {
            "x-max-priority": 200
        }
        channel.queue_declare(self.queue, durable=True, arguments=arguments)
        properties = pika.BasicProperties(delivery_mode=2)
        properties.priority = priority
        channel.basic_publish(exchange='', routing_key=self.queue, body=message,
                              properties=properties)
        connection.close()

    def stop(self):
        pass


def test_producer():
    mq = RabbitMQProducer(host='amqp://guest:o2o@10.198.22.193', queue='mq_key_wx_message')
    # mq = RabbitMQProducer(host='http://10.6.0.137', queue='inte_v2_queue_test2')
    for i in range(5):
        dt = {
            'name': 'migrate_school_paper',
            'message': 'test mq message',
            'msg_type': 'text'
        }
        mq.send_message(message=json.dumps(dt))
        print('success')


def consume_callback(channel, method, propertise, body):
    print('consume a message')
    data = safe_json_decode(body)
    pprint(data)
    channel.basic_ack(delivery_tag=method.delivery_tag)


def test_consumer():
    mq = RabbitMQConsumer(host='amqp://guest:o2o@10.198.22.193', queue='test_queue')
    mq.begin_consume(consume_callback)


def main():
    test_producer()
    # test_consumer()
    # pass


if __name__ == '__main__':
    main()

