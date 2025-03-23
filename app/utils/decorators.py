from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def role_required(role):
    """Restrict access to users with a specific role (e.g., 'admin')."""
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Please log in to access this page.", "warning")
                return redirect(url_for("public.login"))  # adjust this route if needed

            if current_user.role != role:
                flash("You do not have permission to access this page.", "danger")
                return redirect(url_for("public.index"))  # or another fallback

            return view_func(*args, **kwargs)
        return wrapped_view
    return decorator
