from http import HTTPStatus

from fastapi import FastAPI

from fastapi_zero.routers.user_router import router as user_router
from fastapi_zero.schemas.message_schema import Message

app = FastAPI()

app.include_router(user_router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá mundo!'}
