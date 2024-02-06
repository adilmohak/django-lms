import os
import django
from typing import List, Tuple
from django.utils import timezone
from faker import Faker
from factory.django import DjangoModelFactory
from factory import SubFactory, LazyAttribute, Iterator
from django_extensions.management.commands import runscript

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from accounts.models import User, Student, Parent, DepartmentHead, LEVEL, RELATION_SHIP
from course.models import Program

fake = Faker()

class UserFactory(DjangoModelFactory):
    """
    Factory for creating User instances with optional flags.
    
    Attributes:
        username (str): The generated username.
        first_name (str): The generated first name.
        last_name (str): The generated last name.
        email (str): The generated email.
        date_joined (datetime): The current date and time.
        phone (str): The generated phone number.
        address (str): The generated address.
        is_student (bool): Flag indicating if the user is a student.
        is_lecturer (bool): Flag indicating if the user is a lecturer.
        is_parent (bool): Flag indicating if the user is a parent.
        is_dep_head (bool): Flag indicating if the user is a department head.
    """
    
    class Meta:
        model = User

    username: str = LazyAttribute(lambda x: fake.user_name())
    first_name: str = LazyAttribute(lambda x: fake.first_name())
    last_name: str = LazyAttribute(lambda x: fake.last_name())
    email: str = LazyAttribute(lambda x: fake.email())
    date_joined: timezone.datetime = timezone.now()
    phone: str = LazyAttribute(lambda x: fake.phone_number())
    address: str = LazyAttribute(lambda x: fake.address())
    is_student: bool = False
    is_lecturer: bool = False
    is_parent: bool = False
    is_dep_head: bool = False

    @classmethod
    def _create(cls, model_class: type, *args, **kwargs) -> User:
        """
        Create a User instance with optional flags.
        
        Args:
            model_class (type): The class of the model to create.

        Returns:
            User: The created User instance.
        """
        user: User = super()._create(model_class, *args, **kwargs)

        # Set the appropriate flags based on the user type
        if cls.is_student:
            user.is_student = True
        elif cls.is_parent:
            user.is_parent = True

        user.save()
        return user

class ProgramFactory(DjangoModelFactory):
    """
    Factory for creating Program instances.

    Attributes:
        title (str): The generated program title.
        summary (str): The generated summary.
    """

    class Meta:
        model = Program

    title: str = LazyAttribute(lambda x: fake.sentence(nb_words=3))
    summary: str = LazyAttribute(lambda x: fake.text())

    @classmethod
    def _create(cls, model_class: type, *args, **kwargs) -> Program:
        """
        Create a Program instance using get_or_create to avoid duplicates.
        
        Args:
            model_class (type): The class of the model to create.

        Returns:
            Program: The created Program instance.
        """
        program, created = Program.objects.get_or_create(title=kwargs.get("title"), defaults=kwargs)
        return program

class StudentFactory(DjangoModelFactory):
    """
    Factory for creating Student instances with associated User and Program.
    
    Attributes:
        student (User): The associated User instance.
        level (str): The level of the student.
        program (Program): The associated Program instance.
    """

    class Meta:
        model = Student

    student: User = SubFactory(UserFactory, is_student=True)
    level: str = Iterator([choice[0] for choice in LEVEL])
    program: Program = SubFactory(ProgramFactory)

class ParentFactory(DjangoModelFactory):
    """
    Factory for creating Parent instances with associated User, Student, and Program.
    
    Attributes:
        user (User): The associated User instance.
        student (Student): The associated Student instance.
        first_name (str): The generated first name.
        last_name (str): The generated last name.
        phone (str): The generated phone number.
        email (str): The generated email.
        relation_ship (str): The relationship with the student.
    """

    class Meta:
        model = Parent

    user: User = SubFactory(UserFactory, is_parent=True)
    student: Student = SubFactory(StudentFactory)
    first_name: str = LazyAttribute(lambda x: fake.first_name())
    last_name: str = LazyAttribute(lambda x: fake.last_name())
    phone: str = LazyAttribute(lambda x: fake.phone_number())
    email: str = LazyAttribute(lambda x: fake.email())
    relation_ship: str = Iterator([choice[0] for choice in RELATION_SHIP])


def generate_fake_accounts_data(num_programs: int, num_students: int, num_parents: int) -> None:
    """
    Generate fake data for Programs, Students, Parents, and DepartmentHeads.

    Args:
        num_programs (int): Number of programs to generate.
        num_students (int): Number of students to generate.
        num_parents (int): Number of parents to generate.
    """
    programs: List[Program] = ProgramFactory.create_batch(num_programs)
    students: List[Student] = StudentFactory.create_batch(num_students)
    parents: List[Parent] = ParentFactory.create_batch(num_parents)

    print(f"Created {len(programs)} programs.")
    print(f"Created {len(students)} students.")
    print(f"Created {len(parents)} parents.")


generate_fake_accounts_data(10, 10, 10)

