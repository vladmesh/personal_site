import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


# --- Stack ---
class StackRead(BaseModel):
    id: uuid.UUID
    name: str
    icon_url: str | None
    category: str | None
    proficiency: int | None

    model_config = ConfigDict(from_attributes=True)


# --- Work Experience ---
class WorkExperienceTranslationRead(BaseModel):
    language_code: str
    position: str
    description: str
    location: str | None

    model_config = ConfigDict(from_attributes=True)


class WorkExperienceRead(BaseModel):
    id: uuid.UUID
    company_name: str
    company_url: str | None
    start_date: date
    end_date: date | None
    is_current: bool
    translations: list[WorkExperienceTranslationRead]
    stacks: list[StackRead]

    model_config = ConfigDict(from_attributes=True)


# --- Project ---
class ProjectTranslationRead(BaseModel):
    language_code: str
    title: str
    description: str
    role: str | None

    model_config = ConfigDict(from_attributes=True)


class ProjectRead(BaseModel):
    id: uuid.UUID
    slug: str
    link: str | None
    repo_link: str | None
    start_date: date
    end_date: date | None
    is_featured: bool
    translations: list[ProjectTranslationRead]
    stacks: list[StackRead]

    model_config = ConfigDict(from_attributes=True)


# --- Testimonial ---
class TestimonialTranslationRead(BaseModel):
    language_code: str
    author_position: str | None
    content: str

    model_config = ConfigDict(from_attributes=True)


class TestimonialRead(BaseModel):
    id: uuid.UUID
    author_name: str
    author_url: str | None
    author_avatar_url: str | None
    kind: str | None
    date: date
    translations: list[TestimonialTranslationRead]

    model_config = ConfigDict(from_attributes=True)


# --- Contact ---
class ContactTranslationRead(BaseModel):
    language_code: str
    label: str | None

    model_config = ConfigDict(from_attributes=True)


class ContactRead(BaseModel):
    id: uuid.UUID
    type: str
    value: str
    icon: str | None
    is_visible: bool
    sort_order: int
    translations: list[ContactTranslationRead]

    model_config = ConfigDict(from_attributes=True)


# --- Resume ---
class ResumeRead(BaseModel):
    id: uuid.UUID
    language_code: str
    file_path: str
    generated_at: datetime
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


# --- Localized profile payload for frontend ---
class LocalizedWorkExperienceRead(BaseModel):
    id: uuid.UUID
    company_name: str
    company_url: str | None
    start_date: date
    end_date: date | None
    is_current: bool
    position: str
    description: str
    location: str | None
    stacks: list[StackRead]

    model_config = ConfigDict(from_attributes=True)


class LocalizedProjectRead(BaseModel):
    id: uuid.UUID
    slug: str
    link: str | None
    repo_link: str | None
    start_date: date
    end_date: date | None
    is_featured: bool
    title: str
    description: str
    role: str | None
    stacks: list[StackRead]

    model_config = ConfigDict(from_attributes=True)


class LocalizedTestimonialRead(BaseModel):
    id: uuid.UUID
    author_name: str
    author_url: str | None
    author_avatar_url: str | None
    kind: str | None
    date: date
    author_position: str | None
    content: str

    model_config = ConfigDict(from_attributes=True)


class LocalizedContactRead(BaseModel):
    id: uuid.UUID
    type: str
    value: str
    icon: str | None
    sort_order: int
    label: str | None

    model_config = ConfigDict(from_attributes=True)


class ProfileFullRead(BaseModel):
    experience: list[LocalizedWorkExperienceRead]
    projects: list[LocalizedProjectRead]
    stacks: list[StackRead]
    testimonials: list[LocalizedTestimonialRead]
    contacts: list[LocalizedContactRead]
    resumes: list[ResumeRead]
