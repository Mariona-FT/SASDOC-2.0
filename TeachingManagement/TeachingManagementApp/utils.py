from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from functools import wraps

def role_required(allowed_roles=None, redirect_url=None):
    """
    Custom decorator to restrict views based on roles.
    :param allowed_roles: List of roles allowed to access the view.
    :param redirect_url: URL to redirect unauthorized users (if None, raise PermissionDenied).
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return redirect(redirect_url)
        return _wrapped_view
    return decorator
