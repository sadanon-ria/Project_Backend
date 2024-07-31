# ข้อมูลสำหรับผู้รับพัสดุ
def ocr_serializer(item) -> dict:
    return {
        "id": str(item["_id"]),
        "number": item["number"],
        "phone": item["phone"],
        "name": item["name"],
        "company": item["company"],
        "status": item["status"],
        "take": item["take"]
    }

def ocrs_serializer(items) -> list:
    return [ocr_serializer(item) for item in items]

def user_serializer(user) -> dict:
    return {
        "id": str(user["_id"]),
        "number": user["number"],
        "phone": user["phone"],
        "name": user["name"],
        "date": user["date"],
        "company": user["company"],
        "take": user["take"]
    }

def users_serializer(users) -> list:
    return [user_serializer(user) for user in users]

# get ผู้รับ (นักศึกษา) login with line
def parcel_serializer(item) -> dict:
    return{
        "id": str(item["_id"]),
        "name": item["name"]
    }

def parcels_serializer(items) -> list:
    return [parcel_serializer(item) for item in items]
    
# id_token from line
def userToken_serializer(item) -> dict:
    return {
        "id": str(item["_id"]),
        "idToken": item["idToken"],
        "name": item["name"]
    }

def userTokens_serializer(items) -> list:
    return [userToken_serializer(item) for item in items]

def loginUser_serializer(item) -> dict:
    return {
        "id": str(item["_id"]),
        "username": item["username"],
        "password": item["password"],
        "firstname": item["firstname"],
        "lastname": item["lastname"],
        "roles": item["roles"]
    }

def loginUsers_serializer(items) -> list:
    return [loginUser_serializer(item) for item in items]

# ข้อมูลสำหรับผู้ส่งพัสดุ
def express_serializer(item) -> dict:
    return{
        "id": str(item["_id"]),
        "name": item["name"],
        "phone": item["phone"],
        "express": item["express"],
        "parcel": item["parcel"]
    }

def exPress_serializer(items) -> list:
    return [express_serializer(item) for item in items]

def tableExpress_serializer(item) -> dict:
    return {
        "id": str(item["_id"]),
        "date": item["date"],
        "name": item["name"],
        "phone": item["phone"],
        "express": item["express"],
        "parcel": item["parcel"]
    }

def tableExpresss_serializer(items) -> list:
    return [tableExpress_serializer(item) for item in items]
