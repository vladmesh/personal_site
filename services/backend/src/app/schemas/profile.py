import uuid
from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, HttpUrl


# --- Stack ---
class StackRead(BaseModel):
    id: uuid.UUID
    name: str
    icon_url: Optional[str]
    category: Optional[str]
    proficiency: Optional[int]

    model_config = ConfigDict(from_attributes=True)


# --- Work Experience ---
class WorkExperienceTranslationRead(BaseModel):
    language_code: str
    position: str
    description: str
    location: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class WorkExperienceRead(BaseModel):
    id: uuid.UUID
    company_name: str
    company_url: Optional[str]
    start_date: date
    end_date: Optional[date]
    is_current: bool
    translations: List[WorkExperienceTranslationRead]
    stacks: List[StackRead]

    model_config = ConfigDict(from_attributes=True)


# --- Project ---
class ProjectTranslationRead(BaseModel):
    language_code: str
    title: str
    description: str
    role: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class ProjectRead(BaseModel):
    id: uuid.UUID
    slug: str
    link: Optional[str]
    repo_link: Optional[str]
    start_date: date
    end_date: Optional[date]
    is_featured: bool
    translations: List[ProjectTranslationRead]
    stacks: List[StackRead]

    model_config = ConfigDict(from_attributes=True)


# --- Testimonial ---
class TestimonialTranslationRead(BaseModel):
    language_code: str
    author_position: Optional[str]
    content: str

    model_config = ConfigDict(from_attributes=True)


class TestimonialRead(BaseModel):
    id: uuid.UUID
    author_name: str
    author_url: Optional[str]
    author_avatar_url: Optional[str]
    date: date
    translations: List[TestimonialTranslationRead]

    model_config = ConfigDict(from_attributes=True)


# --- Contact ---
class ContactTranslationRead(BaseModel):
    language_code: str
    label: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class ContactRead(BaseModel):
    id: uuid.UUID
    type: str
    value: str
    icon: Optional[str]
    is_visible: bool
    sort_order: int
    translations: List[ContactTranslationRead]

    model_config = ConfigDict(from_attributes=True)


# --- Resume ---
class ResumeRead(BaseModel):
    id: uuid.UUID
    language_code: str
    file_path: str
    generated_at: datetime
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
