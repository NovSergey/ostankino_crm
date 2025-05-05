from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from authx.exceptions import AuthXException
import uvicorn
from starlette import status

from application.backend.api import router as router_backend
from application.backend.api.exceptions import RedirectException
from application.backend.utils.notification_utils import check_unfinished_visits_and_notify
from application.frontend.routers import router as router_frontend
from application.frontend.config import settings as settings_frontend
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.add_job(check_unfinished_visits_and_notify, "cron", hour=20, minute=00)  # каждый день в 18:00
    #scheduler.add_job(check_unfinished_visits_and_notify, "interval", seconds=5)
    scheduler.start()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=router_backend, prefix="/api")
app.include_router(router=router_frontend)

app.mount("/static", StaticFiles(directory=settings_frontend.static_folder), name="static")


@app.exception_handler(AuthXException)
async def exception_token_handler(request: Request, exc: AuthXException):
    if "api" not in str(request.url):
        return RedirectResponse(url="/login/")
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Invalid authentication token"},
    )


@app.exception_handler(RedirectException)
async def exception_redirect_handler(request: Request, exc: RedirectException):
    return RedirectResponse(url=exc.url)


if __name__ == "__main__":
    uvicorn.run("main:app", host="192.168.0.155", port=8080, reload=True)
