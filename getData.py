import logging
from kakaoApi import KakaoApi
from db import Databases

def getSearchKeyword():
    db = Databases()
    result = db.read("restaurant", "id, name, phone_number")
    for id, name, phone in result:
        yield id, name + " " + phone


def getImagesByKakao(place):
    '''
    kakao 이미지 검색 api로 이미지 url 받아오기
    '''
    id, keyword = place
    url = "https://dapi.kakao.com/v2/search/image"
    kakaoApi = KakaoApi()
    kakaoApi.callRequest(url, {"query": keyword, "size": 10})

    db = Databases()
    for place in kakaoApi.response["documents"]:
        db.insert(
            "image", 
            "restaurant_id, type, img_url, img_resource, img_resource_url", 
            ", ".join([
                "\'{}\'".format(id), 
                "\'RESTAURANT\'",
                "\'{}\'".format(place["image_url"]).replace("%", "%%"), 
                "\'{}\'".format(place["display_sitename"]),
                "\'{}\'".format(place["doc_url"]).replace("%", "%%")])
        )
    
k = getSearchKeyword()
while True:
    try:
        getImagesByKakao(next(k))
    except StopIteration as e:
        logging.info(e)
        break
    except Exception as e:
        logging.error(e)
        break