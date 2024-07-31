from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from secrets import token_hex
from config.db import collection_image
from typing import List

route = APIRouter()

@route.post("/upload")
async def upload(files: List[UploadFile] = File(...)):
    # file_ext = files.filename.split(".").pop()
    # file_name = token_hex(10)
    # file_path = f"{file_name}.{file_ext}"

    try:
        files_results = []
        for file in files:
            file_content = await file.read()
            files_results.append({"filename":file.filename, "result": "success"})
            collection_image.insert_one({"filename": file.filename, "data": file_content})
        return JSONResponse(content={"results": files_results}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
    # file_content = await file.read()
    # file_id = await collection_image.fs.files.insert_one({"filename": file.filename})
    # await collection_image.fs.chunks.insert_one({"files_id": file_id.inserted_id, "data": file_content})

    # return {"file_path": file_path}
            

    # collection_image.insert_many
    # with open(file_path, "wb") as f:
    #     content = await file.read()
    #     f.write(content)
    # return 

