from fastapi import FastAPI
import uvicorn
from hm_app.api import auth, profile, house
import redis.asyncio as aioredis
from contextlib import asynccontextmanager
from fastapi_limiter import FastAPILimiter


hm_app = FastAPI(title='homework')

hm_app.include_router(auth.auth_router)
hm_app.include_router(profile.user)
hm_app.include_router(house.house_router)

if __name__ == '__main__':
    uvicorn.run(hm_app, host='127.0.0.1', port=8000)
