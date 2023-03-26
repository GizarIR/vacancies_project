from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import  declarative_base
# from sqlalchemy.orm.decl_api import declarative_base
from sqlalchemy.orm import  sessionmaker
from typing import cast, Any

SQLALCHEMY_DATABASE_URL = "postgresql://root:123@localhost/vacancies"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
# Base = cast(Any, declarative_base())

