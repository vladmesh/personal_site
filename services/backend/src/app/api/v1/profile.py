from collections.abc import Sequence
from typing import Any

from fastapi import APIRouter, Depends, Query
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
    LocalizedContactRead,
    LocalizedProjectRead,
    LocalizedTestimonialRead,
    LocalizedWorkExperienceRead,
    ProfileFullRead,
    ProjectRead,
    ResumeRead,
    StackRead,
    TestimonialRead,
    WorkExperienceRead,
)

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/experience", response_model=list[WorkExperienceRead])
async def get_work_experience(db: AsyncSession = Depends(get_db)) -> Sequence[WorkExperience]:
    """
    Get all work experience entries with translations and stacks.
    """
    result = await db.execute(select(WorkExperience).order_by(WorkExperience.start_date.desc()))
    return result.scalars().all()


@router.get("/projects", response_model=list[ProjectRead])
async def get_projects(db: AsyncSession = Depends(get_db)) -> Sequence[Project]:
    """
    Get all projects with translations and stacks.
    """
    result = await db.execute(
        select(Project).order_by(Project.is_featured.desc(), Project.start_date.desc())
    )
    return result.scalars().all()


@router.get("/stacks", response_model=list[StackRead])
async def get_stacks(db: AsyncSession = Depends(get_db)) -> Sequence[Stack]:
    """
    Get all tech stacks.
    """
    result = await db.execute(select(Stack).order_by(Stack.name))
    return result.scalars().all()


@router.get("/testimonials", response_model=list[TestimonialRead])
async def get_testimonials(db: AsyncSession = Depends(get_db)) -> Sequence[Testimonial]:
    """
    Get all testimonials with translations.
    """
    result = await db.execute(select(Testimonial).order_by(Testimonial.date.desc()))
    return result.scalars().all()


@router.get("/contacts", response_model=list[ContactRead])
async def get_contacts(db: AsyncSession = Depends(get_db)) -> Sequence[Contact]:
    """
    Get all visible contacts with translations.
    """
    result = await db.execute(
        select(Contact).where(Contact.is_visible).order_by(Contact.sort_order)
    )
    return result.scalars().all()


@router.get("/resume", response_model=list[ResumeRead])
async def get_resume(db: AsyncSession = Depends(get_db)) -> Sequence[Resume]:
    """
    Get active resumes.
    """
    result = await db.execute(select(Resume).where(Resume.is_active))
    return result.scalars().all()


@router.get("/full", response_model=ProfileFullRead)
async def get_full_profile(
    lang: str = Query("en", min_length=2, max_length=5, description="Language code, e.g. en or ru"),
    db: AsyncSession = Depends(get_db),
) -> ProfileFullRead:
    """
    Aggregate profile data for a specific language.
    Translations fall back to English, then to the first available translation.
    """
    work_experiences_result = await db.execute(
        select(WorkExperience).order_by(WorkExperience.start_date.desc())
    )
    projects_result = await db.execute(
        select(Project).order_by(Project.is_featured.desc(), Project.start_date.desc())
    )
    stacks_result = await db.execute(select(Stack).order_by(Stack.name))
    testimonials_result = await db.execute(select(Testimonial).order_by(Testimonial.date.desc()))
    contacts_result = await db.execute(
        select(Contact).where(Contact.is_visible).order_by(Contact.sort_order)
    )
    resumes_result = await db.execute(
        select(Resume).where(Resume.is_active).order_by(Resume.language_code)
    )

    work_experiences = [
        _serialize_work_experience(entry, lang) for entry in work_experiences_result.scalars().all()
    ]
    projects = [_serialize_project(entry, lang) for entry in projects_result.scalars().all()]
    stacks = [StackRead.model_validate(entry) for entry in stacks_result.scalars().all()]
    testimonials = [
        _serialize_testimonial(entry, lang) for entry in testimonials_result.scalars().all()
    ]
    contacts = [_serialize_contact(entry, lang) for entry in contacts_result.scalars().all()]
    resumes = [ResumeRead.model_validate(entry) for entry in resumes_result.scalars().all()]

    return ProfileFullRead(
        experience=work_experiences,
        projects=projects,
        stacks=stacks,
        testimonials=testimonials,
        contacts=contacts,
        resumes=resumes,
    )


def _pick_translation(translations: Sequence[Any], lang: str) -> Any | None:
    """Pick translation by lang -> en -> first."""
    for translation in translations:
        if translation.language_code == lang:
            return translation
    for translation in translations:
        if translation.language_code == "en":
            return translation
    return translations[0] if translations else None


def _serialize_work_experience(entry: WorkExperience, lang: str) -> LocalizedWorkExperienceRead:
    translation = _pick_translation(entry.translations, lang)
    return LocalizedWorkExperienceRead(
        id=entry.id,
        company_name=entry.company_name,
        company_url=entry.company_url,
        start_date=entry.start_date,
        end_date=entry.end_date,
        is_current=entry.is_current,
        position=translation.position if translation else "",
        description=translation.description if translation else "",
        location=translation.location if translation else None,
        stacks=[StackRead.model_validate(stack) for stack in entry.stacks],
    )


def _serialize_project(entry: Project, lang: str) -> LocalizedProjectRead:
    translation = _pick_translation(entry.translations, lang)
    return LocalizedProjectRead(
        id=entry.id,
        slug=entry.slug,
        link=entry.link,
        repo_link=entry.repo_link,
        start_date=entry.start_date,
        end_date=entry.end_date,
        is_featured=entry.is_featured,
        title=translation.title if translation else "",
        description=translation.description if translation else "",
        role=translation.role if translation else None,
        stacks=[StackRead.model_validate(stack) for stack in entry.stacks],
    )


def _serialize_testimonial(entry: Testimonial, lang: str) -> LocalizedTestimonialRead:
    translation = _pick_translation(entry.translations, lang)
    return LocalizedTestimonialRead(
        id=entry.id,
        author_name=entry.author_name,
        author_url=entry.author_url,
        author_avatar_url=entry.author_avatar_url,
        kind=entry.kind,
        date=entry.date,
        author_position=translation.author_position if translation else None,
        content=translation.content if translation else "",
    )


def _serialize_contact(entry: Contact, lang: str) -> LocalizedContactRead:
    translation = _pick_translation(entry.translations, lang)
    return LocalizedContactRead(
        id=entry.id,
        type=entry.type,
        value=entry.value,
        icon=entry.icon,
        sort_order=entry.sort_order,
        label=translation.label if translation else None,
    )
