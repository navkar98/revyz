#  Radix Analytics Pvt. Ltd
#  Author : Ravi Vasu
#  Created : 2020-07-23
#  Description : This class contains related to kafka queue services. Kafka is a distributed publish-subscribe
#                messaging system that maintains feeds of messages in partitioned and replicated topics.

"""
Change Log
---------------------------------------------------------------------------
 Date			Author			Comment
---------------------------------------------------------------------------
"""

# System module import
import logging
import json

# Third party module import
from kafka import KafkaConsumer
from kafka import KafkaProducer

# Project module import
from easy.settings import BROKER_URL

# Logger variables to be used for logging
info_logger = logging.getLogger('kafka_info_logger')
error_logger = logging.getLogger('kafka_db_error_logger')


class KafkaQueueService:
    def __init__(self, topic_name, player, group_id=None, enable_auto_commit=False, auto_commit_interval_ms=5000):
        """
        Constructor of the class

        :param topic_name: topic where the message will be published
        :param player: To create object for. Possible values: producer & consumer
        :param group_id: The name of the consumer group to join for dynamic partition assignment (if enabled), and to
                         use for fetching and committing offsets.
        :param enable_auto_commit: If True , the consumer’s offset will be periodically committed in the background.
        :param auto_commit_interval_ms: Number of milliseconds between automatic offset commits, if enable_auto_commit
                                        is True.
        """
        self.url = BROKER_URL
        self.topic_name = topic_name
        self.group_id = group_id
        self.enable_auto_commit = enable_auto_commit
        self.auto_commit_interval_ms = auto_commit_interval_ms
        self.auto_offset_reset = "earliest"
        self.producer = None
        self.consumer = None
        if player == "producer":
            self.load_producer()
        else:
            self.load_consumer()

    def load_producer(self):
        """
        This function is used to create the object of KafkaProducer.
        Producer produce messages to a topic of their choice.

        :return:
        """
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=self.url,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        except Exception as e:
            print("Error during connecting to kafka producer.")
            error_logger.error(e, exc_info=True)

    def load_consumer(self):
        """
        This function is used to create the object of KafkaConsumer.
        Consumers read the messages of a set of partitions of a topic of their choice at their own pace.

        :return:
        """
        try:
            self.consumer = KafkaConsumer(self.topic_name, bootstrap_servers=self.url,
                                          auto_offset_reset=self.auto_offset_reset,
                                          value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                                          group_id=self.group_id, enable_auto_commit=self.enable_auto_commit,
                                          auto_commit_interval_ms=self.auto_commit_interval_ms, max_poll_records=1)
        except Exception as e:
            print("Error during connecting to kafka consumer.")
            error_logger.error(e, exc_info=True)

    def incoming_queue(self, fun_to_run):
        """
        This function is used to read the messages from consumer.

        :param fun_to_run: A user defined function to run for different scenario
        :return:
        """
        try:
            print("type", type(fun_to_run))
            fun_to_run(self.consumer)
        except Exception as e:
            print("Error during receiving message from Kafka.")
            error_logger.error(e, exc_info=True)

    def outgoing_queue(self, outgoing_data, flush=False):
        """
        This function is used to produce (request) a message.

        :param outgoing_data: Message data to be passed in message body
        :param flush: It is used to ensure the message gets sent before the program exits. In normal operation the
                      producer will send messages in batches when it has either accumulated a certain number of
                      messages, or has waited a certain amount of time.
        :return:
        """
        try:
            self.producer.send(self.topic_name, outgoing_data).add_callback(on_send_success).add_errback(on_send_error)
            if flush:
                self.producer.flush()
        except Exception as e:
            print("Error during sending message from Kafka.")
            error_logger.error(e, exc_info=True)


def on_send_success(record_metadata):
    print("topic", record_metadata.topic)
    print("partition", record_metadata.partition)
    print("offset", record_metadata.offset)


def on_send_error(error):
    # handle exception
    print('I am an error callback', error)
    error_logger.error(error, exc_info=True)
