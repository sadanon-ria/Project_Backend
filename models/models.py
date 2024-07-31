from pydantic import BaseModel
from datetime import datetime

# ตอน upload รูปแล้วใช้ ocr ก่อนที่จะนำเข้า database
class ocr(BaseModel):
    number: str
    phone: str
    name: str
    company: str
    status: bool
    take: bool

# ใช้ในหน้าตาราง ได้ข้อมูลจาก model ocr แล้วเพิ่มวันที่
class User(BaseModel):
    number: int
    phone: str
    name: str
    date: datetime
    company: str
    take: bool

# เพิ่มข้อมูล เมื่อขนส่งมาส่งพัสดุที่ห้อง
class express(BaseModel):
    name: str
    phone: str
    express: str
    parcel: int

# ใช้ในหน้าตาราง ได้ข้อมูลจาก model express แล้วเพิ่มวันที่
class tableExpress(BaseModel):
    date: datetime
    name: str
    phone: str
    express: str
    parcel: int

# ใช้ตอน admin เพิ่ม Account ให้พนักงาน
class userAccount(BaseModel):
    username: str
    password: str
    firstname: str
    lastname: str
    roles: str


class parcel(BaseModel):
    to: str

class lineUser(BaseModel):
    idToken: str
    name: str
