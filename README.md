# Learning management system

### I would love to see you contribute 👩‍💻👩‍💻 Feel free to contribute!!

Learning management system using Django and Bootstrap. 

Watch the demo video to find out how the app works https://youtu.be/KKIeRXwZ-Sw

For the quiz part, I used this repo as a reference -> https://github.com/tomwalker/django_quiz

![dj-lms-dashboard](https://user-images.githubusercontent.com/60693922/212262964-5b5f2cb9-59b6-4be8-bf29-63a5265a7a9e.png)

Current features
----------------
* News And Events
* The admin can Add Students
* The admin can Add Lecturers
* Students can Add and Drop courses
* Lecturers submit students score (Attendance, Mid exam, Final exam, assignment)
* The system calculat students Total, Avarage, point, and grade automaticaly
* Also, the system tells the student whether he/she pass, fail or pass with a warning
* Assessment result
* Grade result
* Upload video and documentations for each course
* PDF generator for students registration slip and grade result
* Storing of quiz results under each user
* Question order randomisation
* Previous quiz scores can be viewed on category page
* Correct answers can be shown after each question or all at once at the end
* Logged in users can return to an incomplete quiz to finish it and non-logged in users can complete a quiz if their session persists
* The quiz can be limited to one attempt per user
* Questions can be given a category
* Success rate for each category can be monitored on a progress page
* Explanation for each question result can be given
* Pass marks can be set
* Multiple choice question type
* True/False question type
* Essay question type
* Custom message displayed for those that pass or fail a quiz
* Custom permission (view_sittings) added, allowing users with that permission to view quiz results from users
* A marking page which lists completed quizzes, can be filtered by quiz or user, and is used to mark essay questions

# Installation

First Clone the repo with `git clone https://github.com/adilmohak/django-lms.git`

Run the following command inside the root directory

`pip install -r requirements.txt`

Then open your `settings.py` file and setup your database (name, username, password)

`python manage.py runserver`

Last but not least, go to this address http://127.0.0.1:8000

### Don't forget to give it a star ✨✨
# Thank You!!
