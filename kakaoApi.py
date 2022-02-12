import os
import json
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus

class KakaoApi():
    def callRequest(self, url, params):
        queryParams = {}
        for p in params:
            queryParams[quote_plus(p)] =  params[p]
        queryParams = urlencode(queryParams).encode('ascii')
        self.request = Request(url, queryParams)
        self.request.add_header("Authorization", "KakaoAK " + os.getenv("KAKAO_API_KEY"))

# json.loads(resource.read().decode(resource.headers.get_content_charset("utf8")))
        with urlopen(self.request) as resp:
            self.response = json.loads(resp.read().decode(urlopen(self.request).headers.get_content_charset("utf8")))
