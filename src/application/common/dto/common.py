from datetime import date, datetime
from typing import Union

from pydantic import BaseModel, Extra, validator


class DTO(BaseModel):
    class Config:
        extra = Extra.forbid
        frozen = True


class BirthdayMixin(DTO):
    birthday: Union[date, str]

    @validator("birthday", pre=True)
    def validate_birthday(cls, value):
        if isinstance(value, date):
            return value

        if not isinstance(value, str):
            raise ValueError('birthday must be str "Y-m-d" or date type')

        date_string, *_ = value.split()
        return datetime.strptime(date_string, r"%Y-%m-%d").date()


class AccessDatesMixin(DTO):
    access_start: Union[date, str]
    access_end: Union[date, str]

    @validator("access_start", "access_end", pre=True)
    def validate_dates(cls, value):
        if isinstance(value, date):
            return value

        if not isinstance(value, str):
            raise ValueError('dates must be str "Y-m-d" or date type')

        date_string, *_ = value.split()
        return datetime.strptime(date_string, r"%Y-%m-%d").date()


class AnimalMixin(DTO):
    animal: str

    @validator("animal", pre=True)
    def validate_animal(cls, v):
        if isinstance(v, str):
            return v

        return "###"


class Paginate(BaseModel):
    limit: int
    offset: int
    pages: int
    current_page: int
