import os
import django
import random
from typing import List
from django.utils import timezone
from faker import Faker
from factory.django import DjangoModelFactory
from factory import SubFactory, LazyAttribute, Iterator
from core.models import ActivityLog, NewsAndEvents, Session, Semester, SEMESTER, POST

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

fake = Faker()

class NewsAndEventsFactory(DjangoModelFactory):
    """
    Factory for creating NewsAndEvents instances.

    Attributes:
        title (str): The generated title for the news or event.
        summary (str): The generated summary.
        posted_as (str): The type of the post, either 'News' or 'Event'.
        updated_date (datetime): The generated date and time of update.
        upload_time (datetime): The generated date and time of upload.
    """

    class Meta:
        model = NewsAndEvents

    title: str = LazyAttribute(lambda x: fake.sentence(nb_words=4))
    summary: str = LazyAttribute(lambda x: fake.paragraph(nb_sentences=3))
    posted_as: str = fake.random_element(elements=[choice[0] for choice in POST])
    updated_date: timezone.datetime = fake.date_time_this_year()
    upload_time: timezone.datetime = fake.date_time_this_year()

class SessionFactory(DjangoModelFactory):
    """
    Factory for creating Session instances.

    Attributes:
        session (str): The generated session name.
        is_current_session (bool): Flag indicating if the session is current.
        next_session_begins (date): The date when the next session begins.
    """

    class Meta:
        model = Session

    session: str = LazyAttribute(lambda x: fake.sentence(nb_words=2))
    is_current_session: bool = fake.boolean(chance_of_getting_true=50)
    next_session_begins = LazyAttribute(lambda x: fake.future_datetime())
    

class SemesterFactory(DjangoModelFactory):
    """
    Factory for creating Semester instances.

    Attributes:
        semester (str): The generated semester name.
        is_current_semester (bool): Flag indicating if the semester is current.
        session (Session): The associated session.
        next_semester_begins (date): The date when the next semester begins.
    """

    class Meta:
        model = Semester

    semester: str = fake.random_element(elements=[choice[0] for choice in SEMESTER])
    is_current_semester: bool = fake.boolean(chance_of_getting_true=50)
    session: Session = SubFactory(SessionFactory)
    next_semester_begins = LazyAttribute(lambda x: fake.future_datetime())

class ActivityLogFactory(DjangoModelFactory):
    """
    Factory for creating ActivityLog instances.

    Attributes:
        message (str): The generated log message.
    """

    class Meta:
        model = ActivityLog

    message: str = LazyAttribute(lambda x: fake.text())


def generate_fake_core_data(num_news_and_events: int, num_sessions: int, num_semesters: int, num_activity_logs: int) -> None:
    """
    Generate fake data for core models: NewsAndEvents, Session, Semester, and ActivityLog.

    Args:
        num_news_and_events (int): Number of NewsAndEvents instances to generate.
        num_sessions (int): Number of Session instances to generate.
        num_semesters (int): Number of Semester instances to generate.
        num_activity_logs (int): Number of ActivityLog instances to generate.
    """
    # Generate fake NewsAndEvents instances
    news_and_events: List[NewsAndEvents] = NewsAndEventsFactory.create_batch(num_news_and_events)
    print(f"Generated {num_news_and_events} NewsAndEvents instances.")

    # Generate fake Session instances
    sessions: List[Session] = SessionFactory.create_batch(num_sessions)
    print(f"Generated {num_sessions} Session instances.")

    # Generate fake Semester instances
    semesters: List[Semester] = SemesterFactory.create_batch(num_semesters)
    print(f"Generated {num_semesters} Semester instances.")

    # Generate fake ActivityLog instances
    activity_logs: List[ActivityLog] = ActivityLogFactory.create_batch(num_activity_logs)
    print(f"Generated {num_activity_logs} ActivityLog instances.")

