from datetime import datetime
from datetime import timedelta
import requests
import base64
import sys
   
class PhishTankError(Exception):
    pass
class Result():
    def __init__(self, response):
        self.url = response.get('url', None)
        self.in_database = response.get('in_database', None)
        self.phish_id = response.get('phish_id', None)
        self.phish_detail_page = response.get('phish_detail_page', None)
        self.verified = response.get('verified', None)
        self.valid = response.get('valid', None)
            
    def __phish(self):
        if self.valid:
            return True
        return False
        
class PhishTank():
    __apikey = 'c2450ce424e2ad46756de2e9f0d6572e4053d119661baa48679e547006ba5662'

    def __init__(self, api_url='http://checkurl.phishtank.com/checkurl/', apikey='c2450ce424e2ad46756de2e9f0d6572e4053d119661baa48679e547006ba5662'):
        self.__apikey = apikey
        self._api_url = api_url
            
    def check(self, url):
        post_data = {
            'url': base64.b64encode(url.encode("utf-8")),
            'format': 'json',
            'app_key': self.__apikey,
        }
        response = requests.post(self._api_url, data=post_data)
        data = response.json()

        if 'errortext' in data.keys():
            raise PhishTankError(data['errortext'])
        return Result(data['results'])


            