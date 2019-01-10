from os import path

from twython import Twython


class TweetBot:
    def __init__(self, key_source='values',
                 consumer_key=None, consumer_secret=None,
                 access_token=None, access_token_secret=None):
        if key_source not in ('values', 'files'):
            raise ValueError('key_value should be one of values, files or env')

        consumer_keys = (consumer_key, consumer_secret)
        access_keys = (access_token, access_token_secret)

        if key_source == 'files':
            consumer_keys = list(map(self.read_key_from_file, consumer_keys))
            access_keys = list(map(self.read_key_from_file, access_keys))

        self.api = Twython(*(consumer_keys + access_keys))

        user = self.api.verify_credentials()
        self.screen_name = user['screen_name']
        print('Connected to ' + self.screen_name)

    @staticmethod
    def read_key_from_file(input_file):
        with open(input_file, 'r') as f:
            return f.read()

    def post_photo(self, tweet_text, **kwargs):
        from .camera import EasyCamera

        ec = EasyCamera()
        photo_path = ec.take_photo(path.join(self.screen_name, 'Photos'))

        with open(photo_path, 'rb') as photo:
            upload = self.api.upload_media(media=photo)

        self.api.update_status(
            status=tweet_text, media_ids=[upload['media_id']], **kwargs
        )
        print(
            'Photo at {photo_path} posted to {screen_name}'.format(
                photo_path=photo_path, screen_name=self.screen_name
            )
        )

    def post_video(self, tweet_text, **kwargs):
        from .camera import EasyCamera

        ec = EasyCamera()
        video_path = ec.record_video(path.join(self.screen_name, 'Videos'))

        with open(video_path, 'rb') as video:
            upload = self.api.upload_media(media=video, media_type='video/mp4')

        self.api.update_status(
            status=tweet_text, media_ids=[upload['media_id']], **kwargs
        )

        print(
            'Video at {video_path} posted to {screen_name}'.format(
                video_path=video_path, screen_name=self.screen_name
            )
        )
