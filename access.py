from flask import (
    session,
    request,
    current_app,
    render_template
)
from functools import wraps


def group_validation():
    group = session.get('group_name', None)
    if group is not None and group != '':
        return True
    return False


def group_validation_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if group_validation:
            return f(*args, **kwargs)
        return 'Permission denied'
    return wrapper


def group_permission_validation():
    access_config = current_app.config['ACCESS_CONFIG']
    group_name = session.get('group_name', 'unauthorized')
    target_app = "" if len(request.endpoint.split('.')) == 1 else request.endpoint

    group_name_upd = "unauthorized"
    if type(group_name) is dict:
        group_name_upd = group_name.get('user_role')

    if group_name_upd in access_config:
        if target_app in access_config[group_name_upd]:
            return True
    return False


def group_permission_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if group_permission_validation():
            return f(*args, **kwargs)
        return 'Permission denied'
    return wrapper
