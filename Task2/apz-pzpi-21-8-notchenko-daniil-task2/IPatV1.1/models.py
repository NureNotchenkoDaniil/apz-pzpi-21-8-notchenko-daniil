from tortoise import Model, fields
from pydantic import BaseModel, Field
from datetime import datetime
from tortoise.contrib.pydantic import pydantic_model_creator
from datetime import date
from typing import List, Optional
from tortoise.fields import ManyToManyRelation
from decimal import Decimal


class User(Model):
    id = fields.IntField(pk=True, index=True)
    username = fields.CharField(max_length=50, null=False, unique=True)
    email = fields.CharField(max_length=100, null=False, unique=True)
    password = fields.CharField(max_length=100, null=False)
    is_verified = fields.BooleanField(default=False)
    joined_date = fields.DatetimeField(default=datetime.now())


class Role(Model):
    id = fields.IntField(pk=True, index=True)
    user = fields.ForeignKeyField('models.User', related_name='roles')
    is_admin = fields.BooleanField(default=False)
    is_veterinarian = fields.BooleanField(default=False)
    is_government = fields.BooleanField(default=False)


class PetType(Model):
    id = fields.IntField(pk=True, index=True)
    type_name = fields.CharField(max_length=50, null=False, unique=True)


class Pet(Model):
    id = fields.IntField(pk=True, index=True)
    pet_name = fields.CharField(max_length=50, null=False)
    pet_type = fields.ForeignKeyField('models.PetType', related_name='pets')
    breed = fields.CharField(max_length=100, null=False)
    vaccinated = fields.BooleanField(default=False)
    owner = fields.ForeignKeyField('models.User', related_name='pets')


class StoryOfDisease(Model):
    id = fields.IntField(pk=True, index=True)
    first_visit_date = fields.DateField(null=False)
    last_visit_date = fields.DateField(null=False)
    medications = fields.TextField(null=True)
    pet = fields.ForeignKeyField('models.Pet', related_name='disease_stories')


class PetIn(BaseModel):
    pet_name: str
    pet_type: int
    breed: str
    vaccinated: bool


pet_pydanticIn = PetIn


class StoryOfDiseaseIn(BaseModel):
    first_visit_date: date
    last_visit_date: date
    medications: str = None
    pet: int


story_of_disease_pydanticIn = StoryOfDiseaseIn


class StoryOfDiseaseUpdate(BaseModel):
    first_visit_date: date
    last_visit_date: date
    medications: str = None


story_of_disease_pydanticUpdate = StoryOfDiseaseUpdate


class PetVaccinationUpdate(BaseModel):
    vaccinated: bool


pet_vaccination_update_pydantic = PetVaccinationUpdate


user_pydantic = pydantic_model_creator(User, name='User', exclude=('is_verified', ))
user_pydanticIn = pydantic_model_creator(User, name='UserIn', exclude_readonly=True, exclude=('is_verified', 'join_date'))
user_pydanticOut = pydantic_model_creator(User, name='UserOut', exclude=('password', ))

role_pydantic = pydantic_model_creator(Role, name='Role')
role_pydanticIn = pydantic_model_creator(Role, name='RoleIn', exclude_readonly=True)

pet_type_pydantic = pydantic_model_creator(PetType, name='PetType')
pet_type_pydanticIn = pydantic_model_creator(PetType, name='PetTypeIn', exclude_readonly=True)

pet_pydantic = pydantic_model_creator(Pet, name='Pet')

story_of_disease_pydantic = pydantic_model_creator(StoryOfDisease, name='StoryOfDisease')

