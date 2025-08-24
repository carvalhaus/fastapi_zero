from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from fastapi_zero.services.auth_service import login as login_service


def login(form_data: OAuth2PasswordRequestForm, session: Session):
    return login_service(form_data, session)
