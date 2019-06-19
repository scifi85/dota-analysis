import time
from logging import getLogger

from requests import Session


logger = getLogger(__name__)


class OpenDotaAPI(Session):
    def __init__(self, prefix='https://api.opendota.com/api', retry_timeout=20, retry_on=(429,)):
        self.prefix = prefix
        self.retry_timeout = retry_timeout
        self.retry_on = retry_on
        super().__init__()

    def request(self, method, url, **kwargs):
        while True:
            response = super().request(method=method, url = self.prefix + url, **kwargs)
            if response.status_code in self.retry_on:
                print('Waiting on ', url, response.headers)
                time.sleep(self.retry_timeout)
                continue
            return response
