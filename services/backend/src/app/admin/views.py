"""SQLAdmin ModelView definitions for all models."""

from sqladmin import ModelView

from app.models import (
    Contact,
    ContactTranslation,
    Project,
    ProjectTranslation,
    Resume,
    Stack,
    Testimonial,
    TestimonialTranslation,
    WorkExperience,
    WorkExperienceTranslation,
)


class ProjectAdmin(ModelView, model=Project):
    """Admin view for Project model."""

    column_list = [
        Project.id,
        Project.slug,
        Project.is_featured,
        Project.start_date,
        Project.end_date,
    ]
    column_searchable_list = [Project.slug]
    column_sortable_list = [Project.slug, Project.start_date, Project.is_featured]
    column_default_sort = ("start_date", True)
    form_columns = [
        Project.slug,
        Project.link,
        Project.repo_link,
        Project.start_date,
        Project.end_date,
        Project.is_featured,
        Project.stacks,
    ]
    name = "Project"
    name_plural = "Projects"
    icon = "fa-solid fa-diagram-project"


class ProjectTranslationAdmin(ModelView, model=ProjectTranslation):
    """Admin view for ProjectTranslation model."""

    column_list = [
        ProjectTranslation.id,
        ProjectTranslation.project_id,
        ProjectTranslation.language_code,
        ProjectTranslation.title,
    ]
    column_searchable_list = [ProjectTranslation.title]
    column_sortable_list = [ProjectTranslation.language_code, ProjectTranslation.title]
    form_columns = [
        ProjectTranslation.project,
        ProjectTranslation.language_code,
        ProjectTranslation.title,
        ProjectTranslation.description,
        ProjectTranslation.role,
    ]
    name = "Project Translation"
    name_plural = "Project Translations"
    icon = "fa-solid fa-language"


class WorkExperienceAdmin(ModelView, model=WorkExperience):
    """Admin view for WorkExperience model."""

    column_list = [
        WorkExperience.id,
        WorkExperience.company_name,
        WorkExperience.is_current,
        WorkExperience.start_date,
        WorkExperience.end_date,
    ]
    column_searchable_list = [WorkExperience.company_name]
    column_sortable_list = [
        WorkExperience.company_name,
        WorkExperience.start_date,
        WorkExperience.is_current,
    ]
    column_default_sort = ("start_date", True)
    form_columns = [
        WorkExperience.company_name,
        WorkExperience.company_url,
        WorkExperience.start_date,
        WorkExperience.end_date,
        WorkExperience.is_current,
        WorkExperience.stacks,
    ]
    name = "Work Experience"
    name_plural = "Work Experiences"
    icon = "fa-solid fa-briefcase"


class WorkExperienceTranslationAdmin(ModelView, model=WorkExperienceTranslation):
    """Admin view for WorkExperienceTranslation model."""

    column_list = [
        WorkExperienceTranslation.id,
        WorkExperienceTranslation.work_experience_id,
        WorkExperienceTranslation.language_code,
        WorkExperienceTranslation.position,
    ]
    column_searchable_list = [WorkExperienceTranslation.position]
    column_sortable_list = [
        WorkExperienceTranslation.language_code,
        WorkExperienceTranslation.position,
    ]
    form_columns = [
        WorkExperienceTranslation.work_experience,
        WorkExperienceTranslation.language_code,
        WorkExperienceTranslation.position,
        WorkExperienceTranslation.description,
        WorkExperienceTranslation.location,
    ]
    name = "Work Experience Translation"
    name_plural = "Work Experience Translations"
    icon = "fa-solid fa-language"


class TestimonialAdmin(ModelView, model=Testimonial):
    """Admin view for Testimonial model."""

    column_list = [
        Testimonial.id,
        Testimonial.author_name,
        Testimonial.kind,
        Testimonial.date,
    ]
    column_searchable_list = [Testimonial.author_name]
    column_sortable_list = [Testimonial.author_name, Testimonial.date]
    column_default_sort = ("date", True)
    form_columns = [
        Testimonial.author_name,
        Testimonial.author_url,
        Testimonial.author_avatar_url,
        Testimonial.kind,
        Testimonial.date,
    ]
    name = "Testimonial"
    name_plural = "Testimonials"
    icon = "fa-solid fa-quote-left"


class TestimonialTranslationAdmin(ModelView, model=TestimonialTranslation):
    """Admin view for TestimonialTranslation model."""

    column_list = [
        TestimonialTranslation.id,
        TestimonialTranslation.testimonial_id,
        TestimonialTranslation.language_code,
        TestimonialTranslation.author_position,
    ]
    column_searchable_list = [TestimonialTranslation.author_position]
    column_sortable_list = [
        TestimonialTranslation.language_code,
        TestimonialTranslation.author_position,
    ]
    form_columns = [
        TestimonialTranslation.testimonial,
        TestimonialTranslation.language_code,
        TestimonialTranslation.author_position,
        TestimonialTranslation.content,
    ]
    name = "Testimonial Translation"
    name_plural = "Testimonial Translations"
    icon = "fa-solid fa-language"


class ContactAdmin(ModelView, model=Contact):
    """Admin view for Contact model."""

    column_list = [
        Contact.id,
        Contact.type,
        Contact.value,
        Contact.is_visible,
        Contact.sort_order,
    ]
    column_searchable_list = [Contact.type, Contact.value]
    column_sortable_list = [Contact.type, Contact.sort_order, Contact.is_visible]
    column_default_sort = "sort_order"
    form_columns = [
        Contact.type,
        Contact.value,
        Contact.icon,
        Contact.is_visible,
        Contact.sort_order,
    ]
    name = "Contact"
    name_plural = "Contacts"
    icon = "fa-solid fa-address-book"


class ContactTranslationAdmin(ModelView, model=ContactTranslation):
    """Admin view for ContactTranslation model."""

    column_list = [
        ContactTranslation.id,
        ContactTranslation.contact_id,
        ContactTranslation.language_code,
        ContactTranslation.label,
    ]
    column_searchable_list = [ContactTranslation.label]
    column_sortable_list = [ContactTranslation.language_code, ContactTranslation.label]
    form_columns = [
        ContactTranslation.contact,
        ContactTranslation.language_code,
        ContactTranslation.label,
    ]
    name = "Contact Translation"
    name_plural = "Contact Translations"
    icon = "fa-solid fa-language"


class StackAdmin(ModelView, model=Stack):
    """Admin view for Stack model."""

    column_list = [
        Stack.id,
        Stack.name,
        Stack.category,
        Stack.proficiency,
    ]
    column_searchable_list = [Stack.name, Stack.category]
    column_sortable_list = [Stack.name, Stack.category, Stack.proficiency]
    column_default_sort = "name"
    form_columns = [
        Stack.name,
        Stack.icon_url,
        Stack.category,
        Stack.proficiency,
    ]
    name = "Stack"
    name_plural = "Stacks"
    icon = "fa-solid fa-layer-group"


class ResumeAdmin(ModelView, model=Resume):
    """Admin view for Resume model."""

    column_list = [
        Resume.id,
        Resume.language_code,
        Resume.file_path,
        Resume.is_active,
        Resume.generated_at,
    ]
    column_searchable_list = [Resume.language_code, Resume.file_path]
    column_sortable_list = [Resume.language_code, Resume.is_active, Resume.generated_at]
    column_default_sort = ("generated_at", True)
    form_columns = [
        Resume.language_code,
        Resume.file_path,
        Resume.is_active,
    ]
    name = "Resume"
    name_plural = "Resumes"
    icon = "fa-solid fa-file-pdf"
