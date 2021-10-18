from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus
import os
import xml.etree.ElementTree as elemTree

def getAreaInfoId(typeId):
    '''
    관광 타입에 해당하는 아이템 id를 가져오는 함수
    '''

    result = list() # 반환 결과
    
    # TOURAPI 호출
    url = 'http://api.visitkorea.or.kr/openapi/service/rest/KorService/areaBasedList'
    num=1
    while num<= 2:
        #global response_body2
        queryParams = '?' + urlencode({ quote_plus('ServiceKey') : os.environ.get("TOURAPI_KEY"), 
            quote_plus('pageNo') : num, 
            quote_plus('numOfRows') : '3', 
            quote_plus('MobileApp') : 'AppTest', 
            quote_plus('MobileOS') : 'ETC', 
            quote_plus('contentTypeId') : typeId
            })
        request = Request(url + queryParams)
        request.get_method = lambda: 'GET'
        resource = urlopen(request)
        resp_body = resource.read().decode(resource.headers.get_content_charset('utf8'))
        

        # XML에서 contentid 파싱
        xmlTree = elemTree.fromstring(resp_body).find('./body/items')
        for item in xmlTree.findall('item'):
            result.append(item.find('contentid').text)
        num=num+1
    return result

def getAreaInfo(typeId):
    '''
    관광 타입에 해당하는 관광정보(이름, 주소, 위도, 경도, 전화번호)를 가져오는 함수
    '''

    result = list() # 반환 결과
    
    # TOURAPI 호출
    url = 'http://api.visitkorea.or.kr/openapi/service/rest/KorService/areaBasedList'
    num=1
    while num<= 2:
        #global response_body2
        queryParams = '?' + urlencode({ quote_plus('ServiceKey') : os.environ.get("TOURAPI_KEY"), 
            quote_plus('pageNo') : num, 
            quote_plus('numOfRows') : '1', 
            quote_plus('MobileApp') : 'AppTest', 
            quote_plus('MobileOS') : 'ETC', 
            quote_plus('contentTypeId') : typeId
            })
        request = Request(url + queryParams)
        request.get_method = lambda: 'GET'
        resource = urlopen(request)
        resp_body = resource.read().decode(resource.headers.get_content_charset('utf8'))
        
        # XML에서 contentid 파싱
        xmlTree = elemTree.fromstring(resp_body).find('./body/items')
        for item in xmlTree.findall('item'):
            info = dict()
            info['contentid'] = item.find('contentid').text                            # type id
            info['addr1'] = item.find('addr1').text                 # 상세 주소
            if item.find('firstimage') != None:
                info['firstimage'] = item.find('firstimage').text   # 사진 ID
            else:
                info['firstimage'] = None

            info['mapx'] = item.find('mapx').text                   # 위도
            info['mapy'] = item.find('mapy').text                   # 경도
            info['tel'] = item.find('tel').text                     # 전화번호
            info['title'] = item.find('title').text                 # 이름
            result.append(info)
        num=num+1
        print("지역기반 관광정보:" + str(result))
    return result
        

def getDetailInfo(typeId, contentIds):
    '''
    contentIds에 해당하는 상세정보(운영시간, 요리분류, 주차가능 여부, 휴일)
    '''
    result = list() # 반환 결과
    for id in contentIds:
        # TOURAPI 호출 
        print(id)   
        url = 'http://api.visitkorea.or.kr/openapi/service/rest/KorService/detailIntro'
        queryParams = '?' + urlencode({ quote_plus('ServiceKey') : os.environ.get("TOURAPI_KEY"), 
                quote_plus('pageNo') : '1',  #해당 결과값이 하나밖에 없으니깐 첫번째 페이지로 해둠.
                quote_plus('numOfRows') : '1', 
                quote_plus('MobileApp') : 'AppTest', 
                quote_plus('MobileOS') : 'ETC', 
                quote_plus('contentId') : id,
                quote_plus('contentTypeId') : typeId
            })
        request = Request(url + queryParams)
        request.get_method = lambda: 'GET'
        resource = urlopen(request)
        response_body = resource.read().decode(resource.headers.get_content_charset('utf8'))
        print("소개정보:" + response_body)
        # XML에서 contentid 파싱
        xmlTree = elemTree.fromstring(response_body).find('./body/items')
        for item in xmlTree.findall('item'):
            info = dict()
            info['contentid'] = item.find('contentid').text         # contentid
            info['firstmenu'] = item.find('firstmenu').text         # 요리 분류
            info['opentimefood'] = item.find('opentimefood').text   # 영업 시간
            if "가능" in item.find('parkingfood').text:             # 주차가능 여부
                info['parkingfood'] = True
            else:
                info['parkingfood'] = False
            info['restdatefood'] = item.find('restdatefood').text   # 휴일
            result.append(info)
        print("소개정보:" + str(result))
    return result


def getContentIdByXY(x, y):
    '''
    x,y 좌표에 해당하는 contentid 가져오기
    '''

    result = (None, None) # 반환 결과
    
    print(x, y)
    # TOURAPI 호출
    url = 'http://api.visitkorea.or.kr/openapi/service/rest/KorService/locationBasedList'
    queryParams = '?' + urlencode({ quote_plus('ServiceKey') : os.getenv("TOURAPI_KEY"), 
        quote_plus('pageNo') : 1, 
        quote_plus('numOfRows') : '10', 
        quote_plus('MobileApp') : 'AppTest', 
        quote_plus('MobileOS') : 'ETC', 
        quote_plus('mapX') : x,
        quote_plus('mapY') : y,
        quote_plus('radius') : 1
        })
    request = Request(url + queryParams)
    request.get_method = lambda: 'GET'
    resource = urlopen(request)
    resp_body = resource.read().decode(resource.headers.get_content_charset('utf8'))
    
    # XML에서 contentid 파싱
    xmlTree = elemTree.fromstring(resp_body).find('./body/items')
    for item in xmlTree.findall('item'):
        result = (item.find('contentid').text, item.find('title').text)
    return result


def getContentIdByTitle(title):
    '''
    키워드 검색 API로 타이틀에 헤당하는 contentid 가져오기
    '''

    result = (None, None) # 반환 결과
    
    # TOURAPI 호출
    url = 'http://api.visitkorea.or.kr/openapi/service/rest/KorService/locationBasedList'
    queryParams = '?' + urlencode({ quote_plus('ServiceKey') : os.getenv("TOURAPI_KEY"), 
        quote_plus('pageNo') : 1, 
        quote_plus('numOfRows') : '10', 
        quote_plus('MobileApp') : 'AppTest', 
        quote_plus('MobileOS') : 'ETC', 
        quote_plus('listYN') : 'Y',
        quote_plus('arrange') : 'A',
        quote_plus('contentTypeId') : 39,
        quote_plus('keyword') : title
        })

    print(queryParams)
        
    request = Request(url + queryParams)
    request.get_method = lambda: 'GET'
    resource = urlopen(request)
    resp_body = resource.read().decode(resource.headers.get_content_charset('utf8'))
    print(resp_body)
    # XML에서 contentid 파싱
    xmlTree = elemTree.fromstring(resp_body).find('./body/items')
    for item in xmlTree.findall('item'):
        result = (item.find('contentid').text, item.find('title').text)
    return result

def getImages(contentId):
    '''
    Open API에서 이미지 url 가져오기
    '''

    url = 'http://api.visitkorea.or.kr/openapi/service/rest/KorService/detailImage'
    queryParams = '?' + urlencode({ quote_plus('ServiceKey') : os.environ.get("TOURAPI_KEY"), 
            quote_plus('pageNo') : 1, 
            quote_plus('numOfRows') : '100', 
            quote_plus('MobileApp') : 'AppTest', 
            quote_plus('MobileOS') : 'ETC', 
            quote_plus('contentId') : contentId,
            quote_plus('imageYN') : 'Y',
            quote_plus('subImageYN') : 'Y'
            })
    request = Request(url + queryParams)
    request.get_method = lambda: 'GET'
    resource = urlopen(request)
    resp_body = resource.read().decode(resource.headers.get_content_charset('utf8'))
        
    # XML에서 이미지 url 파싱
    xmlBody = elemTree.fromstring(resp_body).find('./body')
    size = int(xmlBody.find('totalCount').text)
    if size == 0:
        return

    result = list()
    xmlItems = elemTree.fromstring(resp_body).find('./body/items')
    for item in xmlItems.findall('item'):
        result.append(item.find('originimgurl').text)

    
    return result