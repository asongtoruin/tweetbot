from os import path

import tweepy


class TweetBot:
    def __init__(self, key_source='values',
                 consumer_key=None, consumer_secret=None,
                 access_token=None, access_token_secret=None):
        if key_source not in ('values', 'files'):
            raise ValueError('key_value should be one of values, files or env')

        consumer_keys = (consumer_key, consumer_secret)
        access_keys = (access_token, access_token_secret)

        if key_source == 'files':
            consumer_keys = map(self.read_key_from_file, consumer_keys)
            access_keys = map(self.read_key_from_file, access_keys)

        auth = tweepy.OAuthHandler(*consumer_keys)
        auth.set_access_token(*access_keys)

        self.api = tweepy.API(auth)

        user = self.api.me()
        self.screen_name = user.screen_name
        print('Connected to ' + self.screen_name)

    @staticmethod
    def read_key_from_file(input_file):
        with open(input_file, 'r') as f:
            return f.read()

    def post_photo(self, tweet_text, **kwargs):
        from .camera import EasyCamera

        ec = EasyCamera()
        photo_path = ec.take_photo(path.join(self.screen_name, 'Photos'))

        self.api.update_with_media(photo_path, status=tweet_text, **kwargs)
        print(
            'Photo at {photo_path} posted to {screen_name}'.format(
                photo_path=photo_path, screen_name=self.screen_name
            )
        )

    def post_video(self, tweet_text, **kwargs):
        from .camera import EasyCamera

        ec = EasyCamera()
        video_path = ec.record_video(path.join(self.screen_name, 'Videos'))

        self.api.update_with_media(video_path, status=tweet_text, **kwargs)
        print(
            'Video at {video_path} posted to {screen_name}'.format(
                video_path=video_path, screen_name=self.screen_name
            )
        )
