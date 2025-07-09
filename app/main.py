from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.router import api_router
from app.db.pool import get_pool, init_pool
from app.common.exceptions import register_exception_handlers

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)
app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    init_pool()
    await get_pool().open()

@app.on_event("shutdown")
async def shutdown_event():
    await get_pool().close()