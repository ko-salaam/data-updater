from typing import DefaultDict
import connectTourApi as tourapi
from connectDB import Databases


contentType = {'restaurant': '39'}
for typeId in contentType.values():
    contentIds = tourapi.getAreaInfoId(typeId)
    areaInfos = tourapi.getAreaInfo(typeId)
    detailInfos = tourapi.getDetailInfo(typeId, contentIds)

merge_dic = list()
for areaInfo in areaInfos:
    for detailInfo in detailInfos:
        if areaInfo["contentid"] == detailInfo["contentid"]:
            areaInfo.update(detailInfo)
            merge_dic.append(areaInfo)

record_to_insert = (
    merge_dic[0]["title"], 
    merge_dic[0]["mapx"], 
    merge_dic[0]["mapy"], 
    merge_dic[0]["addr1"], 
    merge_dic[0]["tel"], 
    merge_dic[0]["firstmenu"], 
    merge_dic[0]["parkingfood"]
    )

#db 연결
db = Databases()
column = db.readDB()
db.insertDB(
    "restaurant",
    record_to_insert,
    column[1][0],
    column[2][0],
    column[3][0],
    column[4][0],
    column[5][0],
    column[7][0],
    column[11][0]
    )
db.commit()