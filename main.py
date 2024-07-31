from fastapi import FastAPI
from route.upload import route
from OCR.ocr import ocr_router
from route.line import line
from route.login import login
from fastapi.middleware.cors import CORSMiddleware
from config.db import collection_line, collection_image


app = FastAPI()
# app.include_router(route) ไม่ได้ใช้แล้ว
app.include_router(ocr_router)
app.include_router(line)
app.include_router(login)

# Enable CORS (Cross-Origin Resource Sharing) for all routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://test-project-fb777.web.app",
                   "https://cs403.onrender.com/singup",
                   "https://cs403.onrender.com/singin",
                   "https://front-cs-403.vercel.app",
                   "http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

