from datetime import timedelta, datetime
from django.core import signing
from django.core.signing import TimestampSigner


class URL(object):

    def encryption(self, *args, **kwargs):
        time_stamp = TimestampSigner()
        data = signing.dumps(kwargs)
        data = time_stamp.sign(data)
        return data

    def decryption(self, *args, **kwargs):
        time_stamp = TimestampSigner()
        data = kwargs.pop('data', None)
        try:
            data = time_stamp.unsign(data, max_age=3600)
            data = signing.loads(data)
        except Exception as e:
            print(e)
        return data
