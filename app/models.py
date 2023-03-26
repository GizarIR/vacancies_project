from sqlalchemy.orm import relationship
from app.db import Base

import uuid

from sqlalchemy.dialects.postgresql import ARRAY, SMALLINT, UUID
from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    String,
    Text,
)

from app.schemas import SkillDesirability, SkillLevel

class Vacancy(Base):
    __tablename__ = "vacancy"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(254))
    is_active = Column(Boolean, default=False)
    company_id = Column(UUID(as_uuid=True), nullable=False)
    positions = Column(SMALLINT, nullable=False)

    short_description = Column(Text, nullable=True)
    full_description = Column(Text, nullable=True)
    profession_id = Column(UUID(as_uuid=True), nullable=True)

    salary_from = Column(Float, nullable=True)
    salary_to = Column(Float, nullable=True)

    contact_name = Column(String(150), nullable=True)
    contacts = Column(JSON, default=list)

    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    url = Column(String, nullable=True)

    pic_main = Column(String, nullable=True)
    pic_main_dm = Column(String, nullable=True)
    pic_recs = Column(String, nullable=True)

    region = Column(String(50), nullable=True)
    team_ids = Column(ARRAY(UUID(as_uuid=True)), server_default="{}")

    created_on = Column(DateTime(timezone=True), server_default=func.now())
    updated_on = Column(
        DateTime(timezone=True),
        default=func.now(),
        server_onupdate=func.now(),
        onupdate=func.now(),
    )
    skills = relationship(
        "VacancySkill",
        cascade="save-update, merge, delete, delete-orphan",
        passive_deletes=True,
        lazy="raise",
        order_by="desc(VacancySkill.priority)",
    )

    gp_project_id = Column(UUID(as_uuid=True), nullable=True)
    gp_company_id = Column(UUID(as_uuid=True), nullable=True)
    gp_user_id = Column(UUID(as_uuid=True), nullable=True)

    __mapper_args__ = {"eager_defaults": True}


class VacancySkill(Base):
    __tablename__ = "vacancy_skill"
    vacancy_id = Column(UUID(as_uuid=True), ForeignKey("vacancy.id"), primary_key=True)
    skill_id = Column(UUID(as_uuid=True), nullable=False, primary_key=True)
    is_competence = Column(Boolean)
    desirability = Column(Enum(SkillDesirability))
    level = Column(Enum(SkillLevel))
    priority = Column(SMALLINT)
