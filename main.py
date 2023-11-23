from fastapi import FastAPI
from routes.routes import user

api = FastAPI()

api.include_router(user)