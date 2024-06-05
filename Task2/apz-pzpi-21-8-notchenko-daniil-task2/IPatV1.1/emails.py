from fastapi import BackgroundTasks, UploadFile, File, File, Form, Depends, HTTPException, status
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import dotenv_values
from pydantic import BaseModel, EmailStr
from typing import List
from models import User
import jwt

config_credentials = dict(dotenv_values(".env"))

conf = ConnectionConfig(
    MAIL_USERNAME=config_credentials['EMAIL'],
    MAIL_PASSWORD=config_credentials['PASS'],
    MAIL_FROM=config_credentials['EMAIL'],
    MAIL_PORT=2525,
    MAIL_SERVER='sandbox.smtp.mailtrap.io',
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True
)


class EmailSchema(BaseModel):
    email: List[EmailStr]


async def send_email(email: list, instance: User):
    token_data = {
        'id': instance.id,
        'username': instance.username
    }
    token = jwt.encode(token_data, config_credentials['SECRET_KEY'], algorithms=['HS256'])
    #
    template = f"""
        <!DOCTYPE html>
        <html>
            <head></head>
            <body>
                <div style="display: flex; align-items: center; justify-content: content; flex-direction: column">
                    <h3>Account Verification</h3>
                     <br>
                     <p>
                         Thanks for choosing Our Service. Please click on the button below to verify your account.
                    </p>
                    <a style="margin-top: 1rem; padding: 1rem; border-radius: 0.5rem; front-size: 1rem;
                       text-decoration: none" href="http://localhost:8000/verification">
                    Verify your email
                     </a>
                 </div>
            </body>
        </html>
    """
    #
    message = MessageSchema(
        subject='MySite Account Verification Email',
        recipients=email,
        body=template,
        subtype='html'
    )
    #
    fm = FastMail(conf)
    await fm.send_message(message=message)