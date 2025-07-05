from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import os

app = FastAPI(
    title="TimePush API",
    version="0.1.0",
    description="Core API for the TimePush platform"
)

# CORS  
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hello World route
@app.get("/hello", tags=["Hello"])
def hello_world():
    return {"message": "Hello, world!"}

# Health check
@app.get("/", tags=["Health"])
def root():
    return {"message": "TimePush API is running"}


