import os
import logging
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus

class TourApi():
    def __init__(self):
        params = {
            "ServiceKey": os.getenv("TOURAPI_KEYEY"),
            "numOfRows": "3",
            "MobildApp": "AppTest", 
            "MobileOS": "ETC"
        }

    def setRequest(self, url, params):
        queryParams = {}
        for p in params:
            queryParams[quote_plus(p)] =  params[p]
        queryParams = urlencode(queryParams).encode('ascii')
        self.request = Request(url, queryParams)

    def setResponse(self):
        if not self.request: 
            logging.error("request를 먼저 생성해주세요.")

        with urlopen(self.request) as resp:
            self.response = resp.read()
    
    def parseXml(self):
        if not self.response: 
            logging.error("response를 먼저 생성해주세요.")