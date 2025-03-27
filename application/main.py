from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from application.backend.api import router as router_backend
from application.frontend.routers import router as router_frontend
from application.frontend.config import settings as settings_frontend

@asynccontextmanager
async def lifespan(app: FastAPI):
    # async with db_helper.engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=router_backend, prefix="/api")
app.include_router(router=router_frontend)

app.mount("/static", StaticFiles(directory=settings_frontend.static_folder), name="static")


@app.get("/")
async def index():
    return "OK"

if __name__ == "__main__":
    uvicorn.run("main:app", host="192.168.0.155", port=8080, reload=True)