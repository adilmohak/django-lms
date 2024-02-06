from typing import Type
from factory.django import DjangoModelFactory
from factory import SubFactory, LazyAttribute, Iterator
from faker import Faker

from course.models import Program, Course, CourseAllocation,Upload, UploadVideo,CourseOffer, SEMESTER
from accounts.models import User, DepartmentHead
from core.models import Session

from .generate_fake_accounts_data import UserFactory, ProgramFactory
from .generate_fake_core_data import SessionFactory

fake = Faker()

class DepartmentHeadFactory(DjangoModelFactory):
    class Meta:
        model = DepartmentHead

    user = SubFactory(UserFactory)
    department = SubFactory(ProgramFactory)


class ProgramFactory(DjangoModelFactory):
    """
    Factory for creating Program instances.

    Attributes:
        title (str): The generated title for the program.
        summary (str): The generated summary for the program.
    """

    class Meta:
        model = Program

    title: str = LazyAttribute(lambda x: fake.sentence(nb_words=3))
    summary: str = LazyAttribute(lambda x: fake.paragraph())

class CourseFactory(DjangoModelFactory):
    """
    Factory for creating Course instances.

    Attributes:
        slug (str): The generated slug for the course.
        title (str): The generated title for the course.
        code (str): The generated code for the course.
        credit (int): The generated credit for the course.
        summary (str): The generated summary for the course.
        program (Program): The associated program for the course.
        level (str): The generated level for the course.
        year (int): The generated year for the course.
        semester (str): The generated semester for the course.
        is_elective (bool): The flag indicating if the course is elective.
    """

    class Meta:
        model = Course

    slug: str = LazyAttribute(lambda x: fake.slug())
    title: str = LazyAttribute(lambda x: fake.sentence(nb_words=4))
    code: str = LazyAttribute(lambda x: fake.unique.word())
    credit: int = LazyAttribute(lambda x: fake.random_int(min=1, max=6))
    summary: str = LazyAttribute(lambda x: fake.paragraph())
    program: Type[Program] = SubFactory(ProgramFactory)
    level: str = Iterator(["Beginner", "Intermediate", "Advanced"])
    year: int = LazyAttribute(lambda x: fake.random_int(min=1, max=4))
    semester: str = Iterator([choice[0] for choice in SEMESTER])
    is_elective: bool = LazyAttribute(lambda x: fake.boolean())

class CourseAllocationFactory(DjangoModelFactory):
    """
    Factory for creating CourseAllocation instances.

    Attributes:
        lecturer (User): The associated lecturer for the course allocation.
        session (Session): The associated session for the course allocation.
    """

    class Meta:
        model = CourseAllocation

    lecturer: Type[User] = SubFactory(UserFactory, is_lecturer=True)
    session: Type[Session] = SubFactory(SessionFactory)

class UploadFactory(DjangoModelFactory):
    """
    Factory for creating Upload instances.

    Attributes:
        title (str): The generated title for the upload.
        course (Course): The associated course for the upload.
        file (str): The generated file path for the upload.
        updated_date (datetime): The generated updated date for the upload.
        upload_time (datetime): The generated upload time for the upload.
    """

    class Meta:
        model = Upload

    title: str = LazyAttribute(lambda x: fake.sentence(nb_words=3))
    course = SubFactory(CourseFactory)  # Adjust 'yourapp' with your actual app name
    file: str = LazyAttribute(lambda x: fake.file_path(extension="pdf"))
    updated_date = fake.date_time_this_year()
    upload_time = fake.date_time_this_year()

class UploadVideoFactory(DjangoModelFactory):
    """
    Factory for creating UploadVideo instances.

    Attributes:
        title (str): The generated title for the video upload.
        slug (str): The generated slug for the video upload.
        course (Course): The associated course for the video upload.
        video (str): The generated video path for the video upload.
        summary (str): The generated summary for the video upload.
        timestamp (datetime): The generated timestamp for the video upload.
    """

    class Meta:
        model = UploadVideo

    title: str = LazyAttribute(lambda x: fake.sentence(nb_words=3))
    slug: str = LazyAttribute(lambda x: fake.slug())
    course = SubFactory(CourseFactory)  # Adjust 'yourapp' with your actual app name
    video: str = LazyAttribute(lambda x: fake.file_path(extension="mp4"))
    summary: str = LazyAttribute(lambda x: fake.paragraph())
    timestamp = fake.date_time_this_year()

class CourseOfferFactory(DjangoModelFactory):
    """
    Factory for creating CourseOffer instances.

    Attributes:
        dep_head (DepartmentHead): The associated department head for the course offer.
    """

    class Meta:
        model = CourseOffer

    dep_head = SubFactory(DepartmentHeadFactory) 


def generate_fake_course_data(num_programs: int, num_courses: int, num_course_allocations: int, num_uploads: int, num_upload_videos: int, num_course_offers: int) -> None:
    """Generate fake data using various factories.

    Args:
        num_programs (int): Number of fake programs to create.
        num_courses (int): Number of fake courses to create.
        num_course_allocations (int): Number of fake course allocations to create.
        num_uploads (int): Number of fake uploads to create.
        num_upload_videos (int): Number of fake upload videos to create.
        num_course_offers (int): Number of fake course offers to create.
    """
    # Generate fake programs
    programs = ProgramFactory.create_batch(num_programs)
    print(f"Created {len(programs)} programs.")

    # Generate fake courses
    courses = CourseFactory.create_batch(num_courses)
    print(f"Created {len(courses)} courses.")

    # Generate fake course allocations
    course_allocations = CourseAllocationFactory.create_batch(num_course_allocations)
    print(f"Created {len(course_allocations)} course allocations.")

    # Generate fake uploads
    uploads = UploadFactory.create_batch(num_uploads)
    print(f"Created {len(uploads)} uploads.")

    # Generate fake upload videos
    upload_videos = UploadVideoFactory.create_batch(num_upload_videos)
    print(f"Created {len(upload_videos)} upload videos.")

    # Generate fake course offers
    course_offers = CourseOfferFactory.create_batch(num_course_offers)
    print(f"Created {len(course_offers)} course offers.")



generate_fake_course_data(10, 10, 10, 10, 10, 10)