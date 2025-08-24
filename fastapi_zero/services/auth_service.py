from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from fastapi_zero.repositories.auth_repository import login as login_repository


def login(form_data: OAuth2PasswordRequestForm, session: Session):
    return login_repository(form_data, session)
