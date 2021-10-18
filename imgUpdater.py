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

    
getImgFromTour()