import re

from django.conf import settings
from django.contrib.auth.decorators import login_required

class RequireLoginMiddleware(object):
    """
    Middleware component that wraps the login_required decorator around
    matching URL patterns. To use, add the class to MIDDLEWARE_CLASSES and
    define LOGIN_REQUIRED_URLS and LOGIN_REQUIRED_URLS_EXCEPTIONS in your
    settings.py. For example:
    ------
    LOGIN_REQUIRED_URLS = (
        r'/topsecret/(.*)$',
    )
    LOGIN_REQUIRED_URLS_EXCEPTIONS = (
        r'/topsecret/login(.*)$',
        r'/topsecret/logout(.*)$',
    )
    ------
    LOGIN_REQUIRED_URLS is where you define URL patterns; each pattern must
    be a valid regex.

    LOGIN_REQUIRED_URLS_EXCEPTIONS is, conversely, where you explicitly
    define any exceptions (like login and logout URLs).
    """
    def __init__(self):
        self.required = tuple(re.compile(url) for url in settings.LOGIN_REQUIRED_URLS)
        self.exceptions = tuple(re.compile(url) for url in settings.LOGIN_REQUIRED_URLS_EXCEPTIONS)

    def process_view(self, request, view_func, view_args, view_kwargs):
        # No need to process URLs if user already logged in
        if request.user.is_authenticated():
            return None

        # An exception match should immediately return None
        for url in self.exceptions:
            if url.match(request.path):
                return None

        # Requests matching a restricted URL pattern are returned
        # wrapped with the login_required decorator
        for url in self.required:
            if url.match(request.path):
                return login_required(view_func)(request, *view_args, **view_kwargs)

        # Explicitly return None for all non-matching requests
        return None

#adapted from https://gist.github.com/AndrewJHart/9bb9eaea2523cd2144cf959f48a14194
from django.contrib.auth.models import AnonymousUser

from rest_framework.request import Request
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


def get_user_jwt(request):
    """
    Replacement for django session auth get_user & auth.get_user for
     JSON Web Token authentication. Inspects the token for the user_id,
     attempts to get that user from the DB & assigns the user on the
     request object. Otherwise it defaults to AnonymousUser.
    This will work with existing decorators like LoginRequired, whereas
    the standard restframework_jwt auth only works at the view level
    forcing all authenticated users to appear as AnonymousUser ;)
    Returns: instance of user object or AnonymousUser object
    """
    user = None
    try:
        user_jwt = JSONWebTokenAuthentication().authenticate(Request(request))
        if user_jwt is not None:
            print(user_jwt)
            # store the first part from the tuple (user, obj)
            user = user_jwt[0]
    except Exception as error:
        print(error)
        pass

    return user or AnonymousUser()

def jwt_auth_middleware(get_response):
    def middleware(request):
        if not request.user or not request.user.is_authenticated:
            request.user = get_user_jwt(request)
        response = get_response(request)
        return response
    return middleware
