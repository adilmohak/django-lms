from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.test import TestCase, RequestFactory
from accounts.decorators import admin_required

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
        return HttpResponse()

    def test_admin_required_decorator(self):
        # Apply the admin_required decorator to the view function
        decorated_view = admin_required(self.admin_view)
        
        request = self.factory.get("/")
        request.user = self.user
        response = decorated_view(request)
        self.assertEqual(response.status_code, 302)


    def test_admin_required_decorator_with_redirect(self):
        # Apply the admin_required decorator to the view function
        decorated_view = admin_required(function=self.admin_view,redirect_to="/login/")
        
        request = self.factory.get("/")
        request.user = self.user
        response = decorated_view(request)

        # Assert redirection to login page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/')
        
