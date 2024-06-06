from fastapi import FastAPI, Request, HTTPException, status, File, Form, Depends
from tortoise import models
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DoesNotExist
from models import *
from authentication import *
from re import template

# signals
from tortoise.signals import post_save
from typing import List, Optional, Type
from tortoise import BaseDBAsyncClient
# from emails import send_email

# response classes
from fastapi.responses import HTMLResponse

# templates
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse
from fastapi.responses import HTMLResponse

# auth
import jwt
import secrets
from dotenv import dotenv_values
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# self
from fastapi import File, UploadFile
from fastapi.staticfiles import StaticFiles
from PIL import Image

# !cors
from fastapi.middleware.cors import CORSMiddleware

import os
import datetime
from tortoise.transactions import in_transaction


# app create
app = FastAPI()
config_credentials = dict(dotenv_values('.env'))
app.mount("/static", StaticFiles(directory='static'), name="static")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.post('/token')
async def generate_token(request_form: OAuth2PasswordRequestForm = Depends()):
    token = await token_generator(request_form.username, request_form.password)
    return {'access_token': token, 'token_type': 'bearer'}

@app.get('/')
def index():
    return {'Start App': 'OK'}

@app.post('/registration')
async def user_registration(user: user_pydanticIn):
    user_info = user.dict(exclude_unset=True)
    user_info['password'] = get_hashed_password(user_info['password'])
    user_obj = await User.create(**user_info)
    new_user = await user_pydantic.from_tortoise_orm(user_obj)
    return {
        'status': 'ok',
        'data': f'Hello, {new_user.username}! Thanks for registering! Please check your email to confirm your registration.'
    }

@post_save(User)
async def create_role(sender: Type[User], instance: User, created: bool, using_db: Optional[BaseDBAsyncClient], update_fields: List[str]):
    if created:
        await Role.create(user=instance, is_admin=False)
        # send confirmation email
        # await send_email([instance.email], instance)  # -> mailtrap not valid email_addr!!!

@app.get('/verification', response_class=HTMLResponse)
async def email_verification(request: Request, token: str):
    user = await verify_token(token)
    if user and not user.is_verified:
        user.is_verified = True
        await user.save()
        return templates.TemplateResponse('verification.html', {
            'request': request,
            'username': user.username
        })
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid token or expired token',
        headers={'WWW-Authenticate': 'Bearer'}
    )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, config_credentials['SECRET_KEY'], algorithms=['HS256'])
        user = await User.get(id=payload.get('id'))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    return user


@app.post('/user/me')
async def user_login(user: user_pydantic = Depends(get_current_user)):
    pets = await Pet.filter(owner=user)
    roles = await Role.filter(user=user).first()

    return {
        'status': 'Ok',
        'data': {
            'username': user.username,
            'email': user.email,
            'verified': user.is_verified,
            'join_date': user.joined_date.strftime('%d/%m/%Y'),
            'pets': [pet.pet_name for pet in pets],
            'roles': {
                'is_admin': roles.is_admin,
                'is_veterinarian': roles.is_veterinarian,
                'is_government': roles.is_government
            }
        }
    }


@app.post("/pets")
async def create_new_pet(pet: pet_pydanticIn, user: user_pydantic = Depends(get_current_user)):
    pet_info = pet.dict(exclude_unset=True)
    pet_type = await PetType.get(id=pet_info['pet_type'])
    if not pet_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Pet type not found'
        )
    pet_obj = await Pet.create(pet_name=pet_info['pet_name'], breed=pet_info['breed'], vaccinated=pet_info['vaccinated'], owner=user, pet_type=pet_type)
    pet_obj = await pet_pydantic.from_tortoise_orm(pet_obj)
    return {'status': 'OK', 'data': pet_obj}


@app.get('/pets')
async def get_pets(user: user_pydantic = Depends(get_current_user)):
    role = await Role.get(user_id=user.id)
    if role.is_admin or role.is_veterinarian or role.is_government:
        pets = await pet_pydantic.from_queryset(Pet.all())
    else:
        pets = await pet_pydantic.from_queryset(Pet.filter(owner=user))
    return {'status': 'OK', 'data': pets}


@app.get('/pets/{pet_id}')
async def specific_pet(pet_id: int, user: user_pydantic = Depends(get_current_user)):
    try:
        pet = await Pet.get(id=pet_id)
        role = await Role.get(user_id=user.id)

        if pet.owner == user.id or role.is_admin or role.is_veterinarian or role.is_government:
            response = await pet_pydantic.from_tortoise_orm(pet)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Not authenticated to perform this action',
                headers={'WWW-Authenticate': 'Bearer'}
            )

        return {
            'status': 'OK',
            'data': response
        }

    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Pet not found'
        )


@app.put("/pets/{pet_id}/vaccination")
async def update_pet_vaccination(
    pet_id: int,
    pet_update: PetVaccinationUpdate,
    user: user_pydantic = Depends(get_current_user)
):
    role = await Role.get_or_none(user_id=user.id)
    if role is None or not role.is_veterinarian:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You do not have permission to perform this action',
        )

    pet_info = pet_update.dict(exclude_unset=True)
    try:
        pet_obj = await Pet.get(id=pet_id)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Pet not found'
        )

    pet_obj.vaccinated = pet_info['vaccinated']
    await pet_obj.save()
    pet_obj = await pet_pydantic.from_tortoise_orm(pet_obj)
    return {'status': 'OK', 'data': pet_obj}


@app.delete('/pets/{id}')
async def delete_pet(pet_id: int, user: user_pydantic = Depends(get_current_user)):
    pet = await Pet.get(id=pet_id)
    if pet.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Not authenticated to perform this action',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    await pet.delete()
    return {'status': 'OK'}


@app.post("/disease_story")
async def create_disease_story(
    story: StoryOfDiseaseIn,
    user: user_pydantic = Depends(get_current_user)
):
    role = await Role.get(user_id=user.id)
    if not role.is_veterinarian:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Forbidden: Access is restricted to veterinarians only'
        )

    story_info = story.dict(exclude_unset=True)
    pet_id = story_info['pet']

    try:
        pet = await Pet.get(id=pet_id)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Pet not found'
        )

    story_obj = await StoryOfDisease.create(
        first_visit_date=story_info['first_visit_date'],
        last_visit_date=story_info['last_visit_date'],
        medications=story_info.get('medications'),
        pet=pet
    )
    story_obj = await story_of_disease_pydantic.from_tortoise_orm(story_obj)
    return {'status': 'OK', 'data': story_obj}


@app.get('/disease_story')
async def get_disease_stories(user: user_pydantic = Depends(get_current_user)):
    role = await Role.get(user_id=user.id)
    if role.is_admin or role.is_veterinarian or role.is_government:
        response = await story_of_disease_pydantic.from_queryset(StoryOfDisease.all())
    else:
        pets = await Pet.filter(owner=user)
        pet_ids = [pet.id for pet in pets]
        response = await story_of_disease_pydantic.from_queryset(StoryOfDisease.filter(pet_id__in=pet_ids))
    return {'status': 'OK', 'data': response}


@app.get('/disease_story/{id}')
async def specific_disease_story(
    story_id: int,
    user: user_pydantic = Depends(get_current_user)
):
    role = await Role.get(user_id=user.id)
    if not role.is_veterinarian:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Forbidden: Access is restricted to veterinarians only'
        )

    story = await StoryOfDisease.get(id=story_id)
    response = await story_of_disease_pydantic.from_queryset_single(StoryOfDisease.get(id=story_id))
    return {'status': 'OK', 'data': response}


@app.put("/disease_story/{story_id}")
async def update_disease_story(
    story_id: int,
    story_update: StoryOfDiseaseUpdate,
    user: user_pydantic = Depends(get_current_user)
):
    role = await Role.get(user_id=user.id)
    if not role.is_veterinarian:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Forbidden: Access is restricted to veterinarians only'
        )

    story_info = story_update.dict(exclude_unset=True)
    try:
        story_obj = await StoryOfDisease.get(id=story_id)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Disease story not found'
        )

    story_obj.first_visit_date = story_info['first_visit_date']
    story_obj.last_visit_date = story_info['last_visit_date']
    story_obj.medications = story_info.get('medications', story_obj.medications)

    await story_obj.save()
    story_obj = await story_of_disease_pydantic.from_tortoise_orm(story_obj)
    return {'status': 'OK', 'data': story_obj}


@app.delete('/disease_story/{story_id}')
async def delete_disease_story(
    story_id: int,
    user: user_pydantic = Depends(get_current_user)
):
    role = await Role.get(user_id=user.id)
    if not role.is_veterinarian:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Forbidden: Access is restricted to veterinarians only'
        )

    try:
        story = await StoryOfDisease.get(id=story_id)
        await story.delete()
        return {'status': 'OK'}
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Disease story not found'
        )


@app.get('/disease_story/{story_id}/days_between_visits')
async def get_days_between_visits(story_id: int, user: user_pydantic = Depends(get_current_user)):
    try:
        story = await StoryOfDisease.get(id=story_id)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Disease story not found'
        )

    # Check if the user has the necessary permissions
    role = await Role.get(user_id=user.id)
    if not (role.is_admin or role.is_veterinarian or role.is_government or story.pet.owner_id == user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Forbidden: You do not have permission to access this resource'
        )

    days_between_visits = story.get_days_between_visits()
    return {'status': 'OK', 'days_between_visits': days_between_visits}


async def is_admin_user(user: user_pydantic = Depends(get_current_user)):
    role = await Role.get(user_id=user.id)
    if not role.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@app.post("/admin/pet_type")
async def create_pet_type(pet_type: pet_type_pydanticIn, user: user_pydantic = Depends(is_admin_user)):
    pet_type_info = pet_type.dict(exclude_unset=True)
    pet_type_obj = await PetType.create(**pet_type_info)
    pet_type_obj = await pet_type_pydantic.from_tortoise_orm(pet_type_obj)
    return {'status': 'OK', 'data': pet_type_obj}


@app.delete("/admin/pet_type/{pet_type_id}")
async def delete_pet_type(pet_type_id: int, user: user_pydantic = Depends(is_admin_user)):
    try:
        pet_type = await PetType.get(id=pet_type_id)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pet type not found"
        )
    await pet_type.delete()
    return {'status': 'OK'}


#1
async def create_database_backup():
    try:
        current_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        backup_filename = f"backup_{current_datetime}.sql"
        backup_path = os.path.join("backups", backup_filename)

        # Execute backup command
        backup_command = f"mysqldump -u {config_credentials['root']} -p{config_credentials['mysql']} {config_credentials['test_db']} > {backup_path}"
        os.system(backup_command)

        return backup_path
    except Exception as e:
        raise RuntimeError(f"An error occurred while creating backup: {str(e)}")

from fastapi import FastAPI, Depends, HTTPException, status


@app.post("/admin/backup")
async def backup_database(user: user_pydantic = Depends(get_current_user)):
    role = await Role.get(user_id=user.id)
    if not role.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Forbidden: Access is restricted to administrators only'
        )

    backup_path = await create_database_backup()
    return {"status": "OK", "message": f"Backup created successfully: {backup_path}"}


# ** DB connection for MySQL:
CONNECTION_STRING = "mysql://root:mysql@localhost:3306/test_db"
register_tortoise(app, db_url=CONNECTION_STRING, modules={'models': ['models']},
                  generate_schemas=True, add_exception_handlers=True)

