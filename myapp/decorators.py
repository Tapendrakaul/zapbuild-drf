from django.core.exceptions import PermissionDenied
from .models import *

def user_is_admin(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.role_id == ADMIN:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap


def user_is_manager(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.role_id == MANAGER:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap


def user_is_client(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.role_id == CLIENT:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap

def user_is_employee(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.role_id == EMPLOYEE:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap