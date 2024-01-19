from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect


def admin_required(
    function=None,
    redirect_to="/",
):
    """
    Decorator for views that checks that the logged-in user is a superuser,
    redirects to the specified URL if necessary.
    """

    # Define the test function: checks if the user is active and a superuser
    def test_func(user):
        return user.is_active and user.is_superuser

    # Define the wrapper function to handle the response
    def wrapper(request, *args, **kwargs):
        if test_func(request.user):
            # Call the original function if the user passes the test
            return function(request, *args, **kwargs) if function else None
        else:
            # Redirect to the specified URL if the user fails the test
            return redirect(redirect_to)

    return wrapper if function else test_func


def lecturer_required(
    function=None,
    redirect_to="/",
):
    """
    Decorator for views that checks that the logged-in user is a superuser,
    redirects to the specified URL if necessary.
    """

    # Define the test function: checks if the user is active and a superuser
    def test_func(user):
        return user.is_active and user.is_lecturer or user.is_superuser

    # Define the wrapper function to handle the response
    def wrapper(request, *args, **kwargs):
        if test_func(request.user):
            # Call the original function if the user passes the test
            return function(request, *args, **kwargs) if function else None
        else:
            # Redirect to the specified URL if the user fails the test
            return redirect(redirect_to)

    return wrapper if function else test_func


def student_required(
    function=None,
    redirect_to="/",
):
    """
    Decorator for views that checks that the logged-in user is a superuser,
    redirects to the specified URL if necessary.
    """

    # Define the test function: checks if the user is active and a superuser
    def test_func(user):
        return user.is_active and user.is_student or user.is_superuser

    # Define the wrapper function to handle the response
    def wrapper(request, *args, **kwargs):
        if test_func(request.user):
            # Call the original function if the user passes the test
            return function(request, *args, **kwargs) if function else None
        else:
            # Redirect to the specified URL if the user fails the test
            return redirect(redirect_to)

    return wrapper if function else test_func
