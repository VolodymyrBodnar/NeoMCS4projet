import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


from typing import Annotated
from datetime import datetime, timedelta, timezone

from app.scheemas.user import AuthenticatedUser

# openssl rand -hex 32
SECRET_KEY = "sadasdh8213u8kjehsakjdhuiy8y8o"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


credentials_exception = HTTPException(
    status_code=401,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user_name(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> AuthenticatedUser:

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("name")
        role: str = payload.get("role")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    return AuthenticatedUser(role=role, name=username)


async def validate_is_admin_user(
    user: AuthenticatedUser = Depends(get_current_user_name),
) -> None:
    """
    Validate that a user is in the `AdminUser` role in order to access the API.
    Raises a 401 authentication error if not.
    """
    if not "ADMIN" == user.role:
        raise credentials_exception
    return user


async def validate_is_manager(
    user: AuthenticatedUser = Depends(get_current_user_name),
) -> None:
    """
    Validate that a user is in the `MANAGER` role in order to access the API.
    Raises a 401 authentication error if not.
    """
    if not user.role in ["MANAGER", "ADMIN"]:
        raise credentials_exception
    return user


async def validate_is_employee(
    user: AuthenticatedUser = Depends(get_current_user_name),
) -> None:
    """
    Validate that a user is in the `employee` role in order to access the API.
    Raises a 401 authentication error if not.
    """
    if not user.role in ["EMPLOYEE", "MANAGER", "ADMIN"]:
        raise credentials_exception
    return user


AdminUser = Annotated[AuthenticatedUser, Depends(validate_is_admin_user)]
Employee = Annotated[AuthenticatedUser, Depends(validate_is_employee)]
Manager = Annotated[AuthenticatedUser, Depends(validate_is_manager)]
