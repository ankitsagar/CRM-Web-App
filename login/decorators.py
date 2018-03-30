from django.http import Http404
from login.models import User


def check_role(role):
    def _check_role(view_func):
        def wrapped(request, *args, **kwargs):
            if request.user.is_anonymous:
                raise Http404
            u = User.objects.get(username=request.user)
            if u.role == role:
                return view_func(request, *args, **kwargs)
            else:
                raise Http404

        return wrapped
    return _check_role
