# Learning management system using django web framework

Feature-rich learning management system. You may want to build a learning management system(AKA school management system) for a school organization or just for the sake of learning the tech stack and building your portfolio, either way, this project would be a good kickstart for you.

Let's enhance the project by contributing! 👩‍💻👩‍💻

![Screenshot from 2023-12-31 17-36-31]([https://github.com/adilmohak/django-lms/assets/60693922/e7fb628a-6275-4160-ae0f-ab27099ab3ca](https://github.com/mnymkr/django-lms/blob/main/templates/Django_homepage.png)

## Current features

- Dashboard: School demographics and analytics. Restricted to only admins
- News And Events: All users can access this page
- Admin manages students(Add, Update, Delete)
- Admin manages lecturers(Add, Update, Delete)
- Students can Add and Drop courses
- Lecturers submit students' scores: _Attendance, Mid exam, Final exam, assignment_
- The system calculates students' _Total, average, point, and grades automatically_
- Grade comment for each student with a **pass**, **fail**, or **pass with a warning**
- Assessment result page for students
- Grade result page for students
- Session/year and semester management
- Assessments and grades will be grouped by semester
- Upload video and documentation for each course
- PDF generator for students' registration slip and grade result
- Page access restriction
- Storing of quiz results under each user
- Question order randomization
- Previous quiz scores can be viewed on the category page
- Correct answers can be shown after each question or all at once at the end
- Logged-in users can return to an incomplete quiz to finish it and non-logged-in users can complete a quiz if their session persists
- Logged-in users can only view courses and classes that they are assigned to
- The quiz can be limited to one attempt per user
- Questions can be given a category
- Success rate for each category can be monitored on a progress page
- Explanation for each question result can be given
- Pass marks can be set
- Multiple choice question type
- True/False question type
- Essay question type
- Custom message displayed for those that pass or fail a quiz
- Custom permission (view_settings) added, allowing users with that permission to view quiz results from users
- A marking page which lists completed quizzes, can be filtered by quiz or user, and is used to mark essay questions
- A class allocation to allocate lecturers to classes in a course
- A course management to manage the students' enrollment status 

# Quick note for future contributors

If you would like to contribute, simply begin by implementing one from the list in the `TODO.md` file.

# Requirements:

> The following programs are required to run the project

- [Python3.8+](https://www.python.org/downloads/)
- [PostgreSQL database](https://www.postgresql.org/download/)
- [Redis](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/)

# Installation

- Clone the repo with

```bash
git clone https://github.com/adilmohak/django-lms.git
```

- Create and activate a python virtual environment

```bash
pip install -r requirements.txt
```

- Create `.env` file inside the root directory and include the following variables

```bash
# Database config
DB_NAME=[YOUR_DB_NAME]
DB_USER=[DB_ADMIN_NAME]
DB_PASSWORD=[DB_ADMIN_PASSWORD]
DB_HOST=localhost
DB_PORT=[YOUR_POSTGRES_PORT default is 5432]

# Email config
EMAIL_FROM_ADDRESS=Django LMS <youremail@example.com>
EMAIL_HOST_USER=[YOUR_EMAIL]
EMAIL_HOST_PASSWORD=[YOUR_EMAIL_PASSWORD]

# Other
DEBUG=True
SECRET_KEY=[YOUR_SECRET_KEY]
```

```bash
python manage.py migrate
```

```bash
python manage.py createsuperuser
```

```bash
python manage.py runserver
```

Make sure your Redis server is running

```bash
redis-server
```

Start the celery worker

```bash
celery -A config.celery worker -l INFO
```

Last but not least, go to this address http://127.0.0.1:8000 or http://localhost:8000 or http://<your_domain>:8000

### References

- Quiz part: https://github.com/tomwalker/django_quiz

# Connect with me

<div>
<a href="https://github.com/mnymkr" target="_blank">
<img src=https://img.shields.io/badge/github-%2324292e.svg?&style=for-the-badge&logo=github&logoColor=white alt=github style="margin-bottom: 5px;" />
</a>
<a href="https://github.com/HoanNhi" target="_blank">
<img src=https://img.shields.io/badge/github-%2324292e.svg?&style=for-the-badge&logo=github&logoColor=white alt=github style="margin-bottom: 5px;" />
</a>
<a href="https://www.facebook.com/thomastran263/" target="_blank">
<img src=https://img.shields.io/badge/facebook-%232E87FB.svg?&style=for-the-badge&logo=facebook&logoColor=white alt=facebook style="margin-bottom: 5px;" />
</a>
<a href="https://www.facebook.com/thomastran263/" target="_blank">
<img src=https://img.shields.io/badge/facebook-%232E87FB.svg?&style=for-the-badge&logo=facebook&logoColor=white alt=facebook style="margin-bottom: 5px;" />
</a>
</div>

### Help me improve the project and upgrade my trusty old laptop

<p><a href="https://www.buymeacoffee.com/adilmohak"> <img align="left" src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" height="50" width="210" alt="adilmohak" /></a></p><br><br>

#### Show your support by ⭐️ this project!
