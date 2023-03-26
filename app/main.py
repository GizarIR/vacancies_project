from typing import List, Any
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/vacancies/", response_model=schemas.Vacancy)
def create_user(new_vacancy: schemas.CreateVacancy, db: Session = Depends(get_db))->Any:
    # db_vacancy = crud.get_vacancy(db=db, vacancy_id=new_vacancy.id)
    # if db_vacancy:
    #     raise HTTPException(status_code=400, detail="Vacancy already registered")
    return crud.create_vacancy(db=db, vacancy_create=new_vacancy)

@app.get("/vacancies/", response_model=List[schemas.Vacancy])
def read_vacancies(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db))->Any:
    vacancies = crud.get_vacancies(db, skip=skip, limit=limit)
    return vacancies



@app.get("/vacancies/{vacancy_id}", response_model=schemas.Vacancy)
def read_vacancy(vacancy_id: UUID, db: Session = Depends(get_db)):
    db_vacancy = crud.get_vacancy(db, vacancy_id=vacancy_id)
    if db_vacancy is None:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    return db_vacancy
