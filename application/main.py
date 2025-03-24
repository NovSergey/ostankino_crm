from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from core.db_helper import db_helper
from core.models import Base

from api import router as router_api


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=router_api, prefix="/api")


@app.get("/")
async def index():
    return "OK"

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)