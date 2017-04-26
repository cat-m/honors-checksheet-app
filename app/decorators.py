from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

# decorated function to check for unconfirmed users and redirect them to auth.unconfirmed
def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_confirmed is False:
            return redirect(url_for('auth.unconfirmed'))
        return func(*args, **kwargs)
    return decorated_function