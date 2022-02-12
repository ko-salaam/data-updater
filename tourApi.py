import os
import logging
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus

class TourApi():
    def __init__(self):
        self.defaultParams = {
            "ServiceKey": os.getenv("TOURAPI_KEY"),
            "numOfRows": "3",
            "MobildApp": "AppTest", 
            "MobileOS": "ETC"
        }

    def callRequest(self, url, params):
        queryParams = {}
        params.update(self.defaultParams)
        for p in params:
            queryParams[quote_plus(p)] =  params[p]
        queryParams = urlencode(queryParams).encode('ascii')
        self.request = Request(url, queryParams)

        with urlopen(self.request) as resp:
            self.response = resp.read()
    
    def getResponse(self):
        if not self.response: 
            logging.error("response를 먼저 생성해주세요.")
        