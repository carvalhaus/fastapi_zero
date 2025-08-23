from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fastapi_zero.models.user_model import User
from fastapi_zero.schemas.user_schema import UserSchema


def create_user(user: UserSchema, session: Session):
    db_user: User | None = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists',
            )
        if db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='Email already exists'
            )

    db_user = User(
        username=user.username, email=user.email, password=user.password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


def get_users(session: Session, limit: int = 10, offset: int = 0):
    pagination = select(User).limit(limit).offset(offset)
    users = session.scalars(pagination)
    return {'users': users}


def update_user(user_id: int, user: UserSchema, session: Session):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    try:
        db_user.username = user.username
        db_user.email = user.email
        db_user.password = user.password

        session.commit()
        session.refresh(db_user)

        return db_user
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Email already exists'
        )


def get_user(user_id: int, session: Session):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return db_user


def delete_user(user_id: int, session: Session):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    session.delete(db_user)
    session.commit()

    return {'message': 'User deleted'}
