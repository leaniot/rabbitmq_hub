#!/usr/bin/env python
# coding: utf-8
# Author: `mageia`,
# Email: ``,
# Date: `08/05/2017 15:17`
# Description: ''

import time
from django.test import TestCase
from rabbitmq_hub import PubSubHub, Pub, Sub


class RabbitMQTestCase(TestCase):
    @staticmethod
    def user_callback(topic, msg):
        print('user_callback: topic: %s, msg: %s' % (topic, msg))

    def test_hub_publish(self):
        p = PubSubHub(url=['pubsub://127.0.0.1:5672/', 'pubsub://127.0.0.1:5672/'], queue_group='test')
        i = 1
        while True:
            msg = "message: %d" % i
            p.publish(msg, 'leaniot.dashboard.index')
            p.publish(msg, 'leaniot.device.registered')
            i += 1
            print('published %s messages' % (i))
            time.sleep(0.1)

    def test_hub_subscribe(self):
        h = PubSubHub(url=['http://127.0.0.1:5672/', 'http://127.0.0.1:5672/'], queue_group='test')

        h.subscribe('leaniot.user.login', self.user_callback)
        h.subscribe('leaniot.user.logout', self.user_callback)

        @h.subscribe('leaniot.user.login')
        @h.subscribe('leaniot.media.get')
        @h.subscribe('leaniot.media.upload')
        def media_callback(topic, msg):
            print('media_callback: topic: %s, msg: %s' % (topic, msg))
        h.run()
        h.join()

    def test_pub(self):
        p = Pub()
        i = 1

        while True:
            msg = "message: %d" % i
            p.publish(msg, 'leaniot.dashboard.index')
            p.publish(msg, 'leaniot.device.registered')
            # p.publish(msg, 'leaniot.user.logout')
            #
            i += 1
            # msg = {'a': i}
            # p.publish(msg, 'leaniot.media.get')
            #
            # msg = ['aaaa', {'bb': time.time(), 'cc': '121231'}]
            # p.publish(msg, 'leaniot.media.upload')
            # print('published %s messages' % (i))
            time.sleep(0.1)

    def test_sub(self):
        s = Sub('test', '127.0.0.1', reconnect_interval=10)
        s.subscribe('leaniot.user.login', self.user_callback)
        s.subscribe('leaniot.user.logout', self.user_callback)

        @s.subscribe('leaniot.user.login')
        @s.subscribe('leaniot.media.get')
        @s.subscribe('leaniot.media.upload')
        def media_callback(topic, msg):
            print('media_callback: topic: %s, msg: %s' % (topic, msg))
        s.run()

