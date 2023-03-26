import enum
from datetime import date, datetime
# from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl, validator

# from .vacancy_skill import CreateVacancySkillNested, VacancySkillNested


class SortingParam(str, enum.Enum):
    none = "none"
    name = "name"
    profession = "profession"
    created_on = "created_on"
    updated_on = "updated_on"


class SortingOrder(str, enum.Enum):
    asc = "asc"
    desc = "desc"


class SkillLevel(str, enum.Enum):
    EMPTY = "EMPTY"
    INTERN = "INTERN"
    JUNIOR = "JUNIOR"
    MIDDLE = "MIDDLE"
    SENIOR = "SENIOR"
    EXPERT = "EXPERT"


class SkillDesirability(str, enum.Enum):
    REQUIRED = "REQUIRED"
    DESIRED = "DESIRED"
    EMPTY = "EMPTY"


class ContactType(str, enum):
    email = "email"
    telegram = "telegram"
    whatsapp = "whatsapp"
    skype = "skype"
    phone = "phone"
    other = "other"


class Contact(BaseModel):
    type: ContactType
    contact: str


class BaseVacancySkill(BaseModel):
    skill_id: UUID
    is_competence: bool
    desirability: SkillDesirability
    level: SkillLevel
    priority: int

    @validator("priority")
    def validate_smallint(cls, v, values, **kwargs):
        if v < 0:
            raise ValueError("priority must be a positive number")
        if v > 1000:
            raise ValueError("priority number is too large (max 1000)")
        return v

    class Config:
        orm_mode = True


class VacancySkillWithId(BaseModel):
    vacancy_id: UUID


class CreateVacancySkillNested(BaseVacancySkill):
    pass


class VacancySkillNested(BaseVacancySkill):
    pass


class BaseVacancyNoSkills(BaseModel):
    name: str
    is_active: bool = False
    company_id: UUID
    positions: int

    short_description: Optional[str]
    full_description: Optional[str]
    profession_id: Optional[UUID]

    salary_from: Optional[float]
    salary_to: Optional[float]

    contact_name: Optional[str]
    contacts: List[Contact] = Field(default_factory=list)

    start_date: Optional[date]
    end_date: Optional[date]

    url: Optional[HttpUrl] = Field(None, example="http://mycompany.com")

    pic_main: Optional[HttpUrl] = Field(None, example="http://mycompany.com/pic.jpg")
    pic_main_dm: Optional[HttpUrl] = Field(
        None, example="http://mycompany.com/main_pic.png"
    )
    pic_recs: Optional[HttpUrl] = Field(
        None, example="http://mycompany.com/rec_pic.jpg"
    )

    region: Optional[str]

    team_ids: List[UUID] = Field(default_factory=list)

    gp_project_id: Optional[UUID]
    gp_company_id: Optional[UUID]
    gp_user_id: Optional[UUID]

    @validator("salary_to")
    def salary_from_must_be_smaller(cls, v, values, **kwargs):
        salary_from = values.get("salary_from", None)
        if salary_from and v and v < salary_from:
            raise ValueError("salary_from mustn't exceed salary_to")
        return v

    @validator("salary_from")
    def salary_from_large_value(cls, v, values, **kwargs):
        if v and v > 1000000000:
            raise ValueError("salary_from is too large")
        return v

    @validator("salary_to")
    def salary_to_large_value(cls, v, values, **kwargs):
        if v and v > 1000000000:
            raise ValueError("salary_to is too large")
        return v

    @validator("salary_from")
    def salary_from_must_be_positive(cls, v, values, **kwargs):
        if v and v < 0:
            raise ValueError("salary_from cannot be negative number")
        return v

    @validator("salary_to")
    def salary_to_must_be_positive(cls, v, values, **kwargs):
        if v and v < 0:
            raise ValueError("salary_to cannot be negative number")
        return v

    @validator("end_date")
    def end_date_must_be_in_future(cls, v, values, **kwargs):
        start_date = values.get("start_date", None)
        if start_date and v and start_date > v:
            raise ValueError("end_date must be later than start_date")
        return v

    @validator("positions")
    def validate_smallint(cls, v, values, **kwargs):
        if v < 0:
            raise ValueError("positions must be a positive number")
        if v > 3000:
            raise ValueError("positions number is too large (max 3000)")
        return v

    @validator("short_description")
    def validate_short_description(cls, v, values, **kwargs):
        if v and len(v) > 500:
            raise ValueError("short_description can only contain max 500 characters")
        return v

    @validator("short_description")
    def validate_full_description(cls, v, values, **kwargs):
        if v and len(v) > 30000:
            raise ValueError("full_description can only contain max 30000 characters")
        return v

    class Config:
        orm_mode = True


class BaseVacancy(BaseVacancyNoSkills):
    skills: List[VacancySkillNested] = Field(default_factory=list)

    @validator("skills")
    def validate_skills_are_unique(cls, v, values, **kwargs):
        skills = set()
        for skill in v:
            if skill.skill_id in skills:
                raise ValueError("Skills must be unique within 1 vacancy")
            skills.add(skill.skill_id)
        return v


class Vacancy(BaseVacancy):
    id: UUID
    created_on: datetime
    updated_on: datetime


class VacancyPage(BaseModel):
    items: List[Vacancy]
    page: int
    limit: int




class CreateVacancy(BaseVacancy):
    skills: List[CreateVacancySkillNested] = Field(default_factory=list)


class EditVacancy(CreateVacancy):
    id: UUID
    skills: List[VacancySkillNested] = Field(default_factory=list)


class CreateVacancySkill(BaseVacancySkill, VacancySkillWithId):
    pass


class VacancySkill(BaseVacancySkill, VacancySkillWithId):
    pass



