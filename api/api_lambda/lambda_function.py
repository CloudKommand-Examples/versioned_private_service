import boto3
import os
import json
import traceback
from mangum import Mangum

from fastapi import FastAPI, APIRouter, Depends, Request, HTTPException, Header, status, Body, Path, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.security.api_key import APIKeyHeader
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import ExceptionMiddleware

from aws_lambda_powertools import Logger



logger = Logger(service="private-api-v1")

app = FastAPI(
    title="V1 API",
    summary="CloudKommand-deployed V1 API",
    docs_url="/docs",
    root_path="/live",
    version=os.environ.get("VERSION", "1.0.0")
)
app.add_middleware(ExceptionMiddleware, handlers=app.exception_handlers)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


project_router = APIRouter()

@logger.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    return Mangum(app, api_gateway_base_path="/live")(event, context)

@app.exception_handler(Exception)
async def unhandled_exception_handler(request, err):
    logger.exception(f"Unhandled exception in {request.url.path}: {err}")
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

@app.get("/version", tags=["Version"])
async def version() -> str:
    return "V1"


# @app.post("/initialize", tags=["Initialize"])
# def initialize() -> CreateSuccess:
#     return api_initialize()

app.include_router(project_router, prefix="/projects")

