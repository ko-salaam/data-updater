from connectDB import Databases
import connectTourApi as tourapi
import sys

db = Databases()

def updateContentID():
    limit = 400   # row 수
    offset = 0    # 페이지 넘버

    while True:

        # get all restaurants
        restaurants = db.getRestaurants1(limit,offset)
        if len(restaurants) == 0:
            break
        
        # get contentid
        for r in restaurants: 
            contentId, title = tourapi.getContentIdByTitle(r[0])
            if r[0] == title:
                print(db.updateContentId(r[-2], contentId))

        offset += limit

def getImgFromTour():
    '''
    touapi에서 가져올 수 있는 image url 을 DB에 넣음
    '''
    table = "restaurant"
    columns = db.getColumns(table)

    contentIdIndex = columns.index("content_id")
    idIndex = columns.index("id")
    restaurants = db.getTourRestaurants()
    for r in restaurants: 
        imgs = tourapi.getImages(r[contentIdIndex])
        id = r[idIndex]
        if imgs:
            print(db.updateImgUrl(table, id, imgs))

def updateImagesByKakao():
    '''
    KAKAO 이미지 검색 api로 image url 받아와서 DB에 저장
    '''
    table = "accommodation"
    columns = db.getColumns(table)
    phoneIndex = columns.index("phone_number")
    addressIndex = columns.index("address")
    idIndex = columns.index("id")
    places = db.getImgNullPlaces(table)
    for p in places:
        queryWord = p[phoneIndex]
        if not queryWord:
            queryWord = p[addressIndex]

        imgs = tourapi.getImgsFromKakao(queryWord)
        db.updateImgUrl(table, p[idIndex], imgs)


def updateXYByAddress():
    '''
    KAKAO 로컬 api로 DB 좌표 정보 업데이트
    '''
    table = "prayerroom"
    columns = db.getColumns(table)
    addressIndex = columns.index("address")
    for address, id in db.getAddress(table):
        x, y = tourapi.getXYByAddress(address)
        if x and y:
            db.updateXY(table, id, x, y)

updateXYByAddress()


