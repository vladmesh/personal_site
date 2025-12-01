from datetime import date

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.contact import Contact, ContactTranslation
from app.models.project import Project, ProjectTranslation
from app.models.resume import Resume
from app.models.stack import Stack
from app.models.testimonial import Testimonial as TestimonialModel
from app.models.testimonial import TestimonialTranslation
from app.models.work_experience import WorkExperience, WorkExperienceTranslation


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_work_experience_integration(client: AsyncClient, db: AsyncSession) -> None:
    """Integration test: Create work experience and fetch via API using real PostgreSQL."""
    # Create test data
    stack = Stack(name="Python")
    db.add(stack)
    await db.commit()

    exp = WorkExperience(company_name="Test Corp", start_date=date(2023, 1, 1), is_current=True)
    db.add(exp)
    await db.commit()
    await db.refresh(exp)

    # Add translation
    trans = WorkExperienceTranslation(
        work_experience_id=exp.id,
        language_code="en",
        position="Developer",
        description="Wrote code",
    )
    db.add(trans)

    await db.commit()

    # Make real HTTP request
    response = await client.get("/api/v1/profile/experience")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["company_name"] == "Test Corp"
    assert len(data[0]["translations"]) == 1
    assert data[0]["translations"][0]["position"] == "Developer"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_projects_integration(client: AsyncClient, db: AsyncSession) -> None:
    """Integration test: Create project and fetch via API using real PostgreSQL."""
    project = Project(slug="test-project", start_date=date(2023, 1, 1))
    db.add(project)
    await db.commit()
    await db.refresh(project)

    trans = ProjectTranslation(
        project_id=project.id,
        language_code="en",
        title="Test Project",
        description="A test project",
    )
    db.add(trans)
    await db.commit()

    response = await client.get("/api/v1/profile/projects")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["slug"] == "test-project"
    assert data[0]["translations"][0]["title"] == "Test Project"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_stacks_integration(client: AsyncClient, db: AsyncSession) -> None:
    """Integration test: Create stack and fetch via API using real PostgreSQL."""
    stack = Stack(name="FastAPI", category="Backend")
    db.add(stack)
    await db.commit()

    response = await client.get("/api/v1/profile/stacks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "FastAPI"
    assert data[0]["category"] == "Backend"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_testimonials_integration(client: AsyncClient, db: AsyncSession) -> None:
    """Integration test: Create testimonial and fetch via API using real PostgreSQL."""
    testimonial = TestimonialModel(author_name="John Doe", date=date(2023, 1, 1))
    db.add(testimonial)
    await db.commit()
    await db.refresh(testimonial)

    trans = TestimonialTranslation(
        testimonial_id=testimonial.id, language_code="en", content="Great work!"
    )
    db.add(trans)
    await db.commit()

    response = await client.get("/api/v1/profile/testimonials")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["author_name"] == "John Doe"
    assert data[0]["translations"][0]["content"] == "Great work!"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_contacts_integration(client: AsyncClient, db: AsyncSession) -> None:
    """Integration test: Create contact and fetch via API using real PostgreSQL."""
    contact = Contact(type="email", value="test@example.com", is_visible=True)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)

    trans = ContactTranslation(contact_id=contact.id, language_code="en", label="Email")
    db.add(trans)
    await db.commit()

    response = await client.get("/api/v1/profile/contacts")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["value"] == "test@example.com"
    assert data[0]["translations"][0]["label"] == "Email"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_resume_integration(client: AsyncClient, db: AsyncSession) -> None:
    """Integration test: Create resume and fetch via API using real PostgreSQL."""
    resume = Resume(language_code="en", file_path="/tmp/cv.pdf", is_active=True)
    db.add(resume)
    await db.commit()

    response = await client.get("/api/v1/profile/resume")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["file_path"] == "/tmp/cv.pdf"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_full_profile_integration(client: AsyncClient, db: AsyncSession) -> None:
    """Integration test: Aggregate profile data with localization."""
    stack = Stack(name="Python")
    db.add(stack)
    await db.commit()

    exp = WorkExperience(company_name="Test Corp", start_date=date(2023, 1, 1), is_current=True)
    db.add(exp)
    await db.commit()
    await db.refresh(exp)
    exp_trans = WorkExperienceTranslation(
        work_experience_id=exp.id,
        language_code="ru",
        position="Разработчик",
        description="Описание",
        location="Москва",
    )
    exp.stacks.append(stack)
    db.add(exp_trans)

    proj = Project(slug="proj-1", start_date=date(2024, 1, 1))
    db.add(proj)
    await db.commit()
    await db.refresh(proj)
    proj_trans = ProjectTranslation(
        project_id=proj.id,
        language_code="ru",
        title="Проект",
        description="Описание проекта",
        role="Разработчик",
    )
    proj.stacks.append(stack)
    db.add(proj_trans)

    testim = TestimonialModel(author_name="John", date=date(2024, 2, 2))
    db.add(testim)
    await db.commit()
    await db.refresh(testim)
    testim_trans = TestimonialTranslation(
        testimonial_id=testim.id,
        language_code="ru",
        content="Отзыв",
        author_position="Клиент",
    )
    db.add(testim_trans)

    contact = Contact(type="email", value="test@example.com", is_visible=True)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    contact_trans = ContactTranslation(contact_id=contact.id, language_code="ru", label="Почта")
    db.add(contact_trans)

    resume = Resume(language_code="ru", file_path="/tmp/cv_ru.pdf", is_active=True)
    db.add(resume)

    await db.commit()

    response = await client.get("/api/v1/profile/full?lang=ru")
    assert response.status_code == 200
    payload = response.json()
    assert payload["experience"][0]["position"] == "Разработчик"
    assert payload["projects"][0]["title"] == "Проект"
    assert payload["testimonials"][0]["content"] == "Отзыв"
    assert payload["contacts"][0]["label"] == "Почта"
    assert payload["resumes"][0]["language_code"] == "ru"
