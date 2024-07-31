from fastapi import Request, HTTPException, APIRouter
from config.db import collection_image, collection_line, collection_express, collection_userLogin

from fastapi.responses import JSONResponse
from pydantic import BaseModel
import httpx

from linebot.v3.webhook import WebhookParser
from linebot.v3.messaging import (
    AsyncApiClient,
    AsyncMessagingApi,
    Configuration,
    ReplyMessageRequest,
    TextMessage
)
from linebot.models import TextSendMessage

from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)
import requests
from bson import ObjectId
from urllib.parse import urlencode

from models.models import express,lineUser
from schemas.schemas import users_serializer, exPress_serializer, loginUsers_serializer, userTokens_serializer, tableExpresss_serializer

from datetime import datetime, timezone
import pytz

channel_secret = 'e3222b78675e0db46886176fadc83f61'
channel_access_token = 'VWOeAmz+Ps1FzV9GuXV42Tcp7Qa8yQ301/ZGeHGP+TFUC0dWnGWDs0fGQOQfESP6IGHqag+7P3yqOZUfc6+Cq6emmdmvd95naWvtg8rcIZ1lPjdTgdVFn1SPGDqYPJimxN58hfeEyojamcK0nE3adwdB04t89/1O/w1cDnyilFU='

configuration = Configuration(
    access_token=channel_access_token
)

line = APIRouter()
async_api_client = AsyncApiClient(configuration)
line_bot_api = AsyncMessagingApi(async_api_client)
parser = WebhookParser(channel_secret)

class LinePush(BaseModel):
    to: str
    messages: list[dict]

@line.post("/callback")
async def handle_callback(request: Request):
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = await request.body()
    body = body.decode()

    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessageContent):
            continue

        if event.message.text == "ยืนยัน":
            # get userID ของนักศึกษา
            if event.source.type == 'user':
                userId = event.source.user_id
                # เทียบหาใน database
                for data in collection_line.find():
                    if data["idToken"] == userId:
                        name = data["name"]
                        for m in collection_image.find():
                            if name == m["name"] and m["take"] == False:
                                # print("in")
                                collection_image.update_one({"_id": ObjectId(m["_id"])}, {"$set": {"take": True}})

            await line_bot_api.reply_message(
                ReplyMessageRequest(                    
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="ขอบคุณที่ใช้บริการ สามารถเช็คสถานะของตันเองได้ที่ https://front-cs-403.vercel.app/table")]
                )    
            )
    return 'OK'

# @line.put("/test")
# async def test():
#     for data in collection_line.find():
#         if data["idToken"] == "U6282d22487c89a6ccae1c3a32c3c50b1":
#             name = data["name"]
#             # username = collection_image.find_one({"name": name})
#             for m in collection_image.find():
#                 if name == m["name"] and m["take"] == False:
#                     print("in")
#                     collection_image.update_one({"_id": ObjectId(m["_id"])}, {"$set": {"take": True}})       


# @line.post("/push")
async def push_message():
    for data in collection_image.find():
        data_list = []
        line_message = ""
        # เช็ค status ว่า line มีการแจ้งเตือนหรือยัง
        if data["status"] == False:
            # name = data["result"][0] + " " + data["result"][1]
            name = data["name"]
            line_id = collection_line.find_one({"name": name})
            
            detail = collection_image.find_one({"name":name})
            selected_detail = {key: value for key, value in detail.items() if key != "_id"}
            data_list.append(selected_detail)  # เพิ่ม selected_detail เข้าไปในรายการ

            if line_id:
                line_message = "มีพัสดุมาส่งครับ\n"
                for key, value in selected_detail.items():
                    line_message += f"{key}: {value}\n"
                id = line_id["idToken"]
                await push(id, messages=[{"type":"text","text": line_message.strip()}])
                collection_image.update_one({"_id": ObjectId(data["_id"])}, {"$set": {"status": True}})
                data_list = []
                line_message = ""

    return JSONResponse(content={"message": "OK"}, status_code=200)


# @line.post("/test")
# async def test():
#     data_list = []  # สร้างรายการเพื่อเก็บข้อมูลทั้งหมด
#     for data in collection_image.find():
#         if data["status"] == False:
#             name = data["name"]
#             detail = collection_image.find_one({"name": name})
#             # เลือกเฉพาะค่าที่ต้องการจาก detail โดยไม่รวม ObjectId
#             selected_detail = {key: value for key, value in detail.items() if key != "_id"}
#             data_list.append(selected_detail)  # เพิ่ม selected_detail เข้าไปในรายการ

#     return JSONResponse(content={"data": detail}, status_code=200)  # ส่งค่าของ data_list ที่เก็บ selected_detail ทั้งหมดออกไป



async def push(to: str, messages: list[dict]):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer VWOeAmz+Ps1FzV9GuXV42Tcp7Qa8yQ301/ZGeHGP+TFUC0dWnGWDs0fGQOQfESP6IGHqag+7P3yqOZUfc6+Cq6emmdmvd95naWvtg8rcIZ1lPjdTgdVFn1SPGDqYPJimxN58hfeEyojamcK0nE3adwdB04t89/1O/w1cDnyilFU=",  # Replace with your Line API access token
    }
    body = {"to": to, "messages": messages}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.line.me/v2/bot/message/push", headers=headers, json=body
        )
        print(f"status = {response.status_code}")

@line.post("/verify_token")
async def verify(id_token:str):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    params = {
        'id_token': id_token,
        'client_id': '2004090496'
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.line.me/oauth2/v2.1/verify", headers=headers, params=urlencode(params)
        )
        json_response = response.json()
        return json_response
    
# get เฉพาะ ชื่อ
@line.get("/table/{idToken}")
async def get_Oneuser(idToken:str):
    # json_response = await verify(idToken)
    # sub = json_response.get('sub')
    print(idToken)
    all_users = []
    for data in collection_line.find():
        if data["idToken"] == idToken:
            name = data["name"]
            users = collection_image.find({"name": name}, {'_id': False})
            for user in users:
                all_users.append(user)  # เพิ่มข้อมูลที่พบในรายการทั้งหมด

    return {"status": "OK", "data": all_users}
    
# บันทึกเฉพาะ userID 
@line.post("/id_token", tags=["line_user"])
async def post_users(data: lineUser):
    json_response = await verify(data.idToken)
    sub = json_response.get('sub')
    print(sub)
    document = {"idToken": sub, "name": data.name}
    collection_line.insert_one(document)
    return {"status": "OK", "data":userTokens_serializer(collection_line.find())}

# ดูข้อมูลว่ามี user line ใครบ้าง
@line.get("/token", tags=["token"])
async def get_token():
    token = userTokens_serializer(collection_line.find())
    return {"status":"ok", "data":token}

# ค้นหา uid ของคนนั้น
@line.get("/finduid/{idToken}", tags=["token"])
async def find_uid(idToken:str):
    uid = collection_line.find_one({"idToken": idToken}, {'_id': False})
    return {"status": "OK", "data":uid}

# ดูข้อมูลว่ามี user พนักงาน ใครบ้าง
@line.get("/security", tags=["token"])
async def get_security():
    data = loginUsers_serializer(collection_userLogin.find())
    return {"status":"ok", "data":data}

class FollowEvent(BaseModel):
    type: str
    source: dict


@line.get("/get_all_data")
async def get_all_data():
    users = users_serializer(collection_image.find())
    return {"status":"ok", "data":users}

@line.post("/express")
async def post_express(data:express):
    tz_thailand = pytz.timezone('Asia/Bangkok')  # ระบุโซนเวลาของไทย
    utc_now = datetime.now(pytz.utc)  # ดึงเวลาปัจจุบันในโซนเวลา UTC
    thai_now = utc_now.astimezone(tz_thailand)  # แปลงเวลา UTC เป็นเวลาในโซนเวลาของไทย
    modified_data = {
        "date": thai_now.strftime('%d-%m-%Y'),
        "name": data.name,
        "phone": data.phone,
        "express": data.express,
        "parcel": data.parcel
    }
    collection_express.insert_one(dict(modified_data))
    return {"status":"ok", "data":exPress_serializer(collection_express.find())}

@line.get("/getdetail")
async def get_detail():
    detail = tableExpresss_serializer(collection_express.find())
    return {"status":"ok", "data":detail}

@line.post("/post", tags=["user"])
async def post_users(user: lineUser):
    collection_line.insert_one(dict(user))
    return {"status": "OK"}
