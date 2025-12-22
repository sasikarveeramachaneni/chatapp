# from fastapi import FastAPI
# from routes import user
# from routes import chat



# app = FastAPI()

# app.include_router(user.router)
# app.include_router(chat.router)
# @app.get("/")
# def root():
#     return {"status": "Chat App Backend Running"}


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import user, chat

app = FastAPI()

# ✅ THIS IS MANDATORY FOR REACT
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(chat.router)

@app.get("/")
def root():
    return {"status": "Chat App Backend Running"}
