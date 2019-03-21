#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import deque
from datetime import datetime
from pprint import pprint
import sqlite3

from twython import TwythonStreamer

from .helpers import read_key_from_file


class Streamer(TwythonStreamer):
    def __init__(self, queue, key_source='values',
                 consumer_key=None, consumer_secret=None,
                 access_token=None, access_token_secret=None):
        if key_source == 'values':
            super().__init__(
                consumer_key, consumer_secret, access_token, access_token_secret
            )
        else:
            super().__init__(
                *[read_key_from_file(f) for f in (consumer_key, consumer_secret, access_token, access_token_secret)]
            )
        self.queue = queue

    def on_success(self, data):
        if 'text' in data:
            self.queue.append(data)
        else:
            print(data)


class TweetDatabase:
    def __init__(self, db_name, columns_to_store=None, **kwargs):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.queue = deque()

        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS tweets (
                    id integer,
                    created_at text,
                    screen_name text,
                    retweet bool,
                    quote_status bool,
                    tweet_text text,
                    mentions text,
                    hashtags text,
                    language text
                );'''
        )

    def add_tweets(self, tweets):
        print('Adding tweets to database')
        prepared_tweets = [
            (t['id'], t['created_at'], t['user']['screen_name'],
             'retweeted_status' in t, t['is_quote_status'],
             t['text'],
             ','.join(u['screen_name'] for u in t['entities']['user_mentions']),
             ','.join(h['text'] for h in t['entities']['hashtags']),
             t['lang'])
            for t in tweets
        ]
        self.cursor.executemany(
            '''INSERT INTO tweets(
                    id, created_at, screen_name,
                    retweet, quote_status, tweet_text, 
                    mentions, hashtags,
                    language
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);''',
            prepared_tweets
        )

        self.conn.commit()

    def monitor_queue(self, append_size=100):
        while True:
            if len(self.queue) >= append_size:
                tweets = [self.queue.popleft() for _ in range(append_size)]
                print(datetime.now(), 'Adding tweets')
                self.add_tweets(tweets)
                print('Remaining tweets:', len(self.queue))
