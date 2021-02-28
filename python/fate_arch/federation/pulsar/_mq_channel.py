########################################################
# Copyright 2019-2021 program was created VMware, Inc. #
# SPDX-License-Identifier: Apache-2.0                  #
########################################################

import time

import pulsar
from pulsar import _pulsar
from fate_arch.common import log

LOGGER = log.getLogger()
CHANNEL_TYPE_PRODUCER = 'producer'
CHANNEL_TYPE_CONSUMER = 'consumer'
DEFAULT_TENANT = 'fl-tenant'
DEFAULT_CLUSTER = 'standalone'
TOPIC_PREFIX = DEFAULT_TENANT + '/{}/{}'
UNIQUE_PRODUCER_NAME = 'unique_producer'
UNIQUE_CONSUMER_NAME = 'unique_consumer'
DEFAULT_SUBSCRIPTION_NAME = 'unique'


def connection_retry(func):
    """retry connection
    """

    def wrapper(self, *args, **kwargs):
        """wrapper
        """
        res = None
        for ntry in range(60):
            try:
                res = func(self, *args, **kwargs)
                break
            except Exception as e:
                LOGGER.error("function %s error" %
                             func.__name__, exc_info=True)
                time.sleep(0.1)
        return res
    return wrapper

 # A channel cloud only be able to send or receive message.


class MQChannel(object):
    # TODO add credential to secure pulsar cluster
    def __init__(self, host, port, pulsar_namespace, pulsar_send_topic, pulsar_receive_topic, party_id, role, credential=None, extra_args: dict = None):
        # "host:port" is used to connect the pulsar broker
        self._host = host
        self._port = port
        self._namespace = pulsar_namespace
        self._send_topic = pulsar_send_topic
        self._receive_topic = pulsar_receive_topic
        self._credential = credential
        self._party_id = party_id
        self._role = role
        self._extra_args = extra_args

        # "_channel" is the subscriptor for the topic
        self._producer_send = None
        self._producer_conn = None

        self._consumer_receive = None
        self._consumer_conn = None
        self._latest_confirmed = None

        self._producer_config = {}
        if extra_args.get('producer') is not None:
            self._producer_config.update(extra_args['producer'])

        self._consumer_config = {}
        if extra_args.get('consumer') is not None:
            self._consumer_config.update(extra_args['consumer'])

    @property
    def party_id(self):
        return self._party_id

    @connection_retry
    def basic_publish(self, body, properties):
        self._get_or_create_producer()
        LOGGER.debug('send queue: {}'.format(
            self._producer_send.topic()))
        LOGGER.debug(f"send data: {body}")

        self._producer_send.send(content=body, properties=properties)

    @connection_retry
    def consume(self):
        self._get_or_create_consumer()

        LOGGER.debug('receive topic: {}'.format(
            self._consumer_receive.topic()))

        message = self._consumer_receive.receive()
        if message.data() == b'':
            self._consumer_receive.acknowledge(message)
            message = self._consumer_receive.receive()

        self._latest_confirmed = message
        return message

    @connection_retry
    def basic_ack(self, message):
        self._get_or_create_consumer()
        try:
            self._consumer_receive.acknowledge(message)
        except:
            self._consumer_receive.negative_acknowledge(message)

    @connection_retry
    def cancel(self):
        # self._get_or_create_consumer()
        # self._get_or_create_producer()
        try:
            self._consumer_receive.close()
            self._producer_send.close()
        except Exception as e:
            LOGGER.debug('meet {} when trying to close topic'.format(e))

    def _get_or_create_producer(self):
        if self._check_producer_alive() != True:
            self._producer_conn = pulsar.Client(
                'pulsar://{}:{}'.format(self._host, self._port))

            # TODO: it is little bit dangerous to pass _extra_args here ;)
            # TODO: find a batter way to avoid pairs
            self._producer_send = self._producer_conn.create_producer(TOPIC_PREFIX.format(self._namespace, self._send_topic),
                                                                      producer_name=UNIQUE_PRODUCER_NAME,
                                                                      # message_routing_mode=_pulsar.PartitionsRoutingMode.UseSinglePartition,
                                                                      # initial_sequence_id=self._sequence_id,
                                                                      **self._producer_config)

    def _get_or_create_consumer(self):
        if self._check_consumer_alive() != True:
            self._consumer_conn = pulsar.Client(
                'pulsar://{}:{}'.format(self._host, self._port))

            # TODO: it is little bit dangerous to pass _extra_args here ;)
            # TODO: find a batter way to avoid pairs
            self._consumer_receive = self._consumer_conn.subscribe(TOPIC_PREFIX.format(self._namespace, self._receive_topic),
                                                                   subscription_name=DEFAULT_SUBSCRIPTION_NAME,
                                                                   consumer_name=UNIQUE_CONSUMER_NAME,
                                                                   initial_position=_pulsar.InitialPosition.Earliest,
                                                                   **self._consumer_config)

    def _check_producer_alive(self):
        try:
            self._producer_conn.get_topic_partitions("test-alive")
            self._producer_send.send(b'')
            return True
        except Exception:
            if self._producer_conn is not None:
                self._producer_conn.close()
            return False

    def _check_consumer_alive(self):
        try:
            self._consumer_conn.get_topic_partitions("test-alive")
            message = self._consumer_receive.receive(timeout_millis=500)
            self._consumer_receive.negative_acknowledge(message)
            # self._consumer_receive.acknowledge_cumulative(self._latest_confirmed)
            # self._consumer_receive.negative_acknowledge(message)
            return True
        except Exception:
            if self._consumer_conn is not None:
                self._consumer_conn.close()
            return False
