from django.utils import timezone
from datetime import timedelta, datetime
from django.core.signing import TimestampSigner


class URL(object):

    value = dict()
    signer = TimestampSigner()
    age = 20

    def encryption(self, pk, time):
        signer = TimestampSigner()
        self.value = {
            'pk': pk,
            'time': time
        }
        data = signer.sign(self.value)
        print(self.value)
        print(data)
        return data

    def description(self, data):
        self.value = self.signer.unsign(data)
        print(self.value)
        return self.value
