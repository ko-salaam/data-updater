from connectDB import Databases
import connectTourApi as tourapi
import sys

def updateContentID():
    limit = 400   # row 수
    offset = 0    # 페이지 넘버

    while True:

        # get all restaurants
        restaurants = database.getRestaurants1(limit,offset)
        if len(restaurants) == 0:
            break
        
        # get contentid
        for r in restaurants: 
            contentId, title = tourapi.getContentIdByTitle(r[0])
            if r[0] == title:
                print(database.updateContentId(r[-2], contentId))

        offset += limit

    
database = Databases()