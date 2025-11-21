from typing import List, Sequence

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.contact import Contact
from app.models.project import Project
from app.models.resume import Resume
from app.models.stack import Stack
from app.models.testimonial import Testimonial
from app.models.work_experience import WorkExperience
from app.schemas.profile import (
    ContactRead,
    ProjectRead,
    ResumeRead,
    StackRead,
    TestimonialRead,
    WorkExperienceRead,
)

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/experience", response_model=List[WorkExperienceRead])
async def get_work_experience(db: AsyncSession = Depends(get_db)) -> Sequence[WorkExperience]:
    """
    Get all work experience entries with translations and stacks.
    """
    result = await db.execute(
        select(WorkExperience).order_by(WorkExperience.start_date.desc())
    )
    return result.scalars().all()


@router.get("/projects", response_model=List[ProjectRead])
async def get_projects(db: AsyncSession = Depends(get_db)) -> Sequence[Project]:
    """
    Get all projects with translations and stacks.
    """
    result = await db.execute(
        select(Project).order_by(Project.is_featured.desc(), Project.start_date.desc())
    )
    return result.scalars().all()


@router.get("/stacks", response_model=List[StackRead])
async def get_stacks(db: AsyncSession = Depends(get_db)) -> Sequence[Stack]:
    """
    Get all tech stacks.
    """
    result = await db.execute(select(Stack).order_by(Stack.name))
    return result.scalars().all()


@router.get("/testimonials", response_model=List[TestimonialRead])
async def get_testimonials(db: AsyncSession = Depends(get_db)) -> Sequence[Testimonial]:
    """
    Get all testimonials with translations.
    """
    result = await db.execute(select(Testimonial).order_by(Testimonial.date.desc()))
    return result.scalars().all()


@router.get("/contacts", response_model=List[ContactRead])
async def get_contacts(db: AsyncSession = Depends(get_db)) -> Sequence[Contact]:
    """
    Get all visible contacts with translations.
    """
    result = await db.execute(
        select(Contact)
        .where(Contact.is_visible == True)
        .order_by(Contact.sort_order)
    )
    return result.scalars().all()


@router.get("/resume", response_model=List[ResumeRead])
async def get_resume(db: AsyncSession = Depends(get_db)) -> Sequence[Resume]:
    """
    Get active resumes.
    """
    result = await db.execute(
        select(Resume).where(Resume.is_active == True)
    )
    return result.scalars().all()
