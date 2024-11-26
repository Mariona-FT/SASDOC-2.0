from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

def role_required(allowed_roles=None, redirect_url=None):
    """
    Custom decorator to restrict views based on roles.
    :param allowed_roles: List of roles allowed to access the view.
    :param redirect_url: URL to redirect unauthorized users (if None, raise PermissionDenied).
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if allowed_roles and request.user.role not in allowed_roles:
                if redirect_url:
                    return redirect(redirect_url)
                else:
                    raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
