from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.test import TestCase, RequestFactory
from accounts.decorators import admin_required, lecturer_required, student_required

User = get_user_model()

class AdminRequiredDecoratorTests(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='password'
        )
        self.user = User.objects.create_user(
            username='user', email='user@example.com', password='password'
        )
        self.factory = RequestFactory()
    
    def admin_view(self, request):
        return HttpResponse("Admin View Content")

    def test_admin_required_decorator_redirects(self):
        decorated_view = admin_required(self.admin_view)
        
        request = self.factory.get("/restricted-view")
        request.user = self.user
        response = decorated_view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")


    def test_admin_required_decorator_redirects_to_correct_path(self):
        decorated_view = admin_required(function=self.admin_view,redirect_to="/login/")
        
        request = self.factory.get("restricted-view")
        request.user = self.user
        response = decorated_view(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/')
    
    def test_admin_required_decorator_does_not_redirect_superuser(self):
        decorated_view = admin_required(self.admin_view)
        
        request = self.factory.get("/restricted-view")
        request.user = self.superuser
        response = decorated_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Admin View Content")
    
    def test_admin_redirect_decorator_return_correct_response(self):
        decorated_view = admin_required(self.admin_view)
        
        request = self.factory.get("/restricted-view")
        request.user = self.superuser
        response = decorated_view(request)
        self.assertIsInstance(response, HttpResponse)


class LecturerRequiredDecoratorTests(TestCase):
    def setUp(self):
        self.lecturer = User.objects.create_user(
            username='lecturer', email='lecturer@example.com', password='password', is_lecturer=True
        )
        self.user = User.objects.create_user(
            username='user', email='user@example.com', password='password'
        )
        self.factory = RequestFactory()

    def lecturer_view(self, request):
        return HttpResponse("Lecturer View Content")

    def test_lecturer_required_decorator_redirects(self):
        decorated_view = lecturer_required(self.lecturer_view)

        request = self.factory.get("/restricted-view")
        request.user = self.user

        response = decorated_view(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    def test_lecturer_required_decorator_redirects_to_correct_path(self):
        decorated_view = lecturer_required(function=self.lecturer_view, redirect_to="/login/")

        request = self.factory.get("/restricted-view")
        request.user = self.user

        response = decorated_view(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/')

    def test_lecturer_required_decorator_does_not_redirect_lecturer(self):
        decorated_view = lecturer_required(self.lecturer_view)

        request = self.factory.get("/restricted-view")
        request.user = self.lecturer

        response = decorated_view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Lecturer View Content")

    def test_lecturer_redirect_decorator_return_correct_response(self):
        decorated_view = lecturer_required(self.lecturer_view)

        request = self.factory.get("/restricted-view")
        request.user = self.lecturer

        response = decorated_view(request)

        self.assertIsInstance(response, HttpResponse)

class StudentRequiredDecoratorTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(
            username='student', email='student@example.com', password='password', is_student=True
        )
        self.user = User.objects.create_user(
            username='user', email='user@example.com', password='password'
        )
        self.factory = RequestFactory()

    def student_view(self, request):
        return HttpResponse("Student View Content")

    def test_student_required_decorator_redirects(self):
        # Apply the student_required decorator to the view function
        decorated_view = student_required(self.student_view)

        # Create a mock request object with a non-student user
        request = self.factory.get("/restricted-view")
        request.user = self.user

        # Call the decorated view
        response = decorated_view(request)

        # Assert that the response is a redirect (status code 302)
        self.assertEqual(response.status_code, 302)
        # Assert that the response redirects to the default URL ("/")
        self.assertEqual(response.url, "/")

    def test_student_required_decorator_redirects_to_correct_path(self):
        # Apply the student_required decorator to the view function
        decorated_view = student_required(function=self.student_view, redirect_to="/login/")

        # Create a mock request object with a non-student user
        request = self.factory.get("/restricted-view")
        request.user = self.user

        # Call the decorated view
        response = decorated_view(request)

        # Assert redirection to login page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/')

    def test_student_required_decorator_does_not_redirect_student(self):
        # Apply the student_required decorator to the view function
        decorated_view = student_required(self.student_view)

        # Create a mock request object with a student user
        request = self.factory.get("/restricted-view")
        request.user = self.student

        # Call the decorated view
        response = decorated_view(request)

        # Assert that the response is not a redirect (status code 200)
        self.assertEqual(response.status_code, 200)
        # Assert that the response contains the view content
        self.assertEqual(response.content, b"Student View Content")

    def test_student_redirect_decorator_return_correct_response(self):
        # Apply the student_required decorator to the view function
        decorated_view = student_required(self.student_view)

        # Create a mock request object with a student user
        request = self.factory.get("/restricted-view")
        request.user = self.student

        # Call the decorated view
        response = decorated_view(request)

        # Assert that the response is an instance of HttpResponse
        self.assertIsInstance(response, HttpResponse)