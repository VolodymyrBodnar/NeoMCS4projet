from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


from ..services.user import get_user, register_user, authenticate_user, update_user_role
from ..scheemas.user import UserCreate, UserDetail, UserAuth, AuthenticatedUser
from ..dependencies.auth import create_access_token, get_current_user_name

from ..database import get_db_session
from uuid import uuid4

import os
from dotenv import load_dotenv

load_dotenv()


HOST_EMAIL = os.getenv('HOST_EMAIL')
APP_PASS = os.getenv('APP_PASS')

router = APIRouter()


@router.post("/login/")
def read_items(user: UserAuth):
    authenticated_user = authenticate_user(user)
    if authenticated_user is not None:
        token = create_access_token(
            {"name": authenticated_user.name, "role": authenticated_user.role}
        )
        return {"token": token}
    else:
        raise HTTPException(status_code=404)


@router.post("/register/")
def new_user(user: UserCreate, db=Depends(get_db_session)):
    register_user(
        db,
        user=user,
    )
    send_virification_email(user.email)
    return 200


@router.get("/users/{user_id}")
def retriewe_user(user_id: int, db=Depends(get_db_session)) -> UserDetail:
    user = get_user(user_id=user_id, db=db)
    return user


@router.post("/users/")
def set_role(user_data: AuthenticatedUser):
    update_user_role(user_data)
    return 200

def send_virification_email(email):
    otp = str(uuid4())
    msg = MIMEMultipart()
    msg['From'] = HOST_EMAIL
    msg['To'] = email
    msg['Subject'] = 'simple email in python'
    message = f'Your OTP IS: {otp}'
    msg.attach(MIMEText(message))

    mailserver = smtplib.SMTP('smtp.gmail.com',587)
    # identify ourselves to smtp gmail client
    mailserver.ehlo()
    # secure our email with tls encryption
    mailserver.starttls()
    # re-identify ourselves as an encrypted connection
    mailserver.ehlo()
    mailserver.login(HOST_EMAIL, APP_PASS)

    mailserver.sendmail(HOST_EMAIL,email,msg.as_string())

    mailserver.quit()
    