

from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user


def turi_buti_atsijunges(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            flash("Jūs jau prisijungę.", "info")
            print("PRISIJUNGES")
            return redirect(url_for("index"))
        return func(*args, **kwargs)

    return decorated_function

def Roles_Patikrinimas(roles : list[str]):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.vaidmuo not in roles:
                flash("Jūs neturite privilegijų.", "info")
                return redirect(url_for("error_403"))
            return func(*args, **kwargs)
        return wrapper
    return decorator