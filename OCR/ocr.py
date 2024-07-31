# import cv2
# import easyocr
# import time

# # เริ่มจับเวลา
# start_time = time.time()
# # image = cv2.imread(r'C:/Users/Admin/Desktop/project/image/parcel/good/3.jpg')
# image = cv2.imread(r'C:/Users/Admin/Desktop/project/image/parcel/New folder/40.jpg')
# # cv2.imshow('image',image)

# image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# # cv2.imshow('image_gray',image_gray)

# image_wb = cv2.threshold(image_gray, 100, 255, cv2.THRESH_BINARY)[1]
# # cv2.imshow('image_wb', image_wb)

# reader = easyocr.Reader(['th'],gpu = True)
# result = reader.readtext(image,detail=0)
# # หยุดจับเวลา
# end_time = time.time()

# print(result)

# # คำนวณและแสดงเวลาที่ใช้ในการประมวลผล
# processing_time = end_time - start_time
# print("เวลาที่ใช้ในการประมวลผล: {:.2f} วินาที".format(processing_time))
# cv2.waitKey(0)
# cv2.destroyAllWindows
# print("**********************************************************************************")

# import cv2
# import easyocr
# import numpy as np
# import re

# Replace with your image path
# รูปทดสอบ
# image_path = "C:/Users/Admin/Desktop/project/image/parcel/01_testOCR.png"
# image_path = "C:/Users/Admin/Desktop/project/1.png"

#  path รูปกล่องพัสดุ
# image_path = "C:/Users/Admin/Desktop/project/image/parcel/flash/1.jpg"
# image_path = "C:/Users/Admin/Desktop/project/image/parcel/S__9994248.jpg"

# image_path = "C:/Users/Admin/Desktop/project/image/parcel/S__9994247.jpg"
# image_path = "C:/Users/Admin/Desktop/project/image/parcel/S__9994247_test.png"

# Load and pre-process the image
# image = cv2.imread(image_path)
# image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# image_wb = cv2.threshold(image_gray, 100, 255, cv2.THRESH_BINARY)[1]
# cv2.imshow('image_wb', image_wb)
# cv2.waitKey(0)
# cv2.destroyAllWindows


# version ที่ใช้ได้

# Perform OCR and filter results
# reader = easyocr.Reader(['th'])
# results = reader.readtext(image_wb, detail=0)
# print(results)
# # Process OCR results
# ocr_results = []
# count = 0
# for x in results:
#     text = re.search(r'(นาย|นาง|รับ|ถึง|ชาวโลก)', x)
#     if text and re.search(r'[ก-๙a-zA-Z]+ [ก-๙a-zA-Z]+',results[count+1]):
#         print(results[count+1])
#     else:
#         count = count + 1

# print("**********************************************************************************")

# for result in results:
#     # print("OCR Result:", result)
#     try:
#         # ที่ใช้ result[1] เพราะมันมีโครงสร้าง (location, text, confidence) แบบนี้ 
#         # ไม่น่าใช่แบบบน
#         # text = result[1]
#         # print(result) \s+([\w\s]+   นาย|นางสาว?|นาง|รับ|ถึง|ชาวโลก
#         match = re.search(r'(นาย|นางสาว?|นาง|รับ|ถึง|ชาวโลก)', result)
#         # name = match.group(2)
#         print(f"Extracted name: {match}")
#         ocr_results.append(match)
#         # มันไม่เข้าเงื่อนไข if
#         if match:
#             # เป็นการรวมกลุ่มของ (นาย|นางสาว?|นาง|ผู้รับ|ถึง|สวัสดิชาวโลก) และ \s+([\w\s]+)
#             print("if true")
#             name = match.group(2)
#             print(f"Extracted name: {name}")
#             ocr_results.append(name)
#     except IndexError as e:
#         print(f"Error: {e} - Unable to extract name from result: {result}")
# print (ocr_results)
# print("**********************************************************************************")


# import base64
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from config.db import collection_image
from models.models import ocr
from schemas.schemas import ocrs_serializer
from route.line import push_message

from typing import List
import cv2
import easyocr
import numpy as np
import re
from datetime import datetime, timezone
import pytz


ocr_router = APIRouter()

def process_ocr(image_content):
    
    # Convert image content to numpy array
    nparr = np.frombuffer(image_content, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Perform OCR
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_wb = cv2.threshold(image_gray, 100, 255, cv2.THRESH_BINARY)[1]
    reader = easyocr.Reader(['th'], gpu=True)

    # อ่านข้อความจากภาพ
    results = reader.readtext(image_wb, detail=0)
    # เช็ค output
    # print(results)
    # Process OCR results
    ocr_results = []
    count = 0
    for x in results:
        text = re.search(r'(นาย|นาง|รับ|ถึง|ถง)', x)
        if text and re.search(r'[ก-๙a-zA-Z]+ [ก-๙a-zA-Z]+',results[count+1]):
            ocr_results.append(results[count+1])
            # print(results[count+1])
        else:
            count = count + 1
    
    print(results)
    print()
    print(ocr_results)
    # return results
    return ocr_results


@ocr_router.post("/perform-ocr-multiple")
async def perform_ocr_multiple(files: List[UploadFile] = File(...)):
    try:
        ocr_results = []
        for file in files:
            image_content = await file.read()
            ocr_result = process_ocr(image_content)
            # ocr_results.append({"filename": file.filename, "result": ocr_result})
            ocr_results.append({"result": ocr_result})
            # print(ocr_results)
            # collection_image.insert_one({"filename": file.filename, "result": ocr_result, "status":False})

        return JSONResponse(content={"results": ocr_results}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
@ocr_router.post("/addocr")
async def add_ocr(data: ocr):
    tz_thailand = pytz.timezone('Asia/Bangkok')  # ระบุโซนเวลาของไทย
    utc_now = datetime.now(pytz.utc)  # ดึงเวลาปัจจุบันในโซนเวลา UTC
    thai_now = utc_now.astimezone(tz_thailand)  # แปลงเวลา UTC เป็นเวลาในโซนเวลาของไทย
    modified_data = {
        "number": data.number,
        "phone": data.phone,
        "name": data.name,
        # datetime.now(timezone.utc)
        "date": thai_now.strftime('%d-%m-%Y'),
        "company": data.company,
        "status": False,
        "take": False
    }
    collection_image.insert_one(dict(modified_data))
    await push_message()
    # date จะเข้าไปอยู่ใน mongoDB แล้ว แต่ตอน return ออกมาจะไม่มีเพราะไม่ได้ใส่ใน model เพราะไม่จำเป็นให้ front ส่งมา
    return {"status":"ok", "data":ocrs_serializer(collection_image.find())}
