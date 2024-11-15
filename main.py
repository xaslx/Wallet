from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from exceptions import InvalidJson
from src.api.v1.auth import router as auth_router
from src.api.v1.wallet import router as wallet_router
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware



@asynccontextmanager
async def lifespan(app: FastAPI):
    yield



app: FastAPI = FastAPI(lifespan=lifespan)

app.include_router(auth_router, prefix='/api/v1/auth')
app.include_router(wallet_router, prefix='/api/v1/wallets')


origins = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    raise InvalidJson()
