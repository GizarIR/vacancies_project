from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session, selectinload
from sqlalchemy.future import select


from app import models, schemas

from app.models import Vacancy, VacancySkill

def get_vacancies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vacancy).offset(skip).limit(limit).all()

def get_vacancy(db: Session, vacancy_id: UUID) -> Optional[Vacancy]:
    return db.query(models.Vacancy).filter(models.Vacancy.id == vacancy_id).first()

def create_vacancy(db: Session, vacancy_create: schemas.CreateVacancy) -> Vacancy:
    vacancy_dict = vacancy_create.dict()
    skills = vacancy_dict.pop("skills")
    new_vacancy = Vacancy(**vacancy_dict)
    db.add(new_vacancy)
    db.commit()

    for skill in skills:
        db.add(VacancySkill(**skill, vacancy_id=new_vacancy.id))
    db.commit()

    # db.refresh(vacancy_create)
    return get_vacancy(db, new_vacancy.id)
