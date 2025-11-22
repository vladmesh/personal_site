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
