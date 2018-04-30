from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import logout, update_session_auth_hash
from django.http import Http404, HttpResponseRedirect

# Create your views here.

@login_required()
def verify_login(request):
    print(request.user.role)
    if request.user.role == 'Manager':
        return HttpResponseRedirect(reverse_lazy("manager:dashboard"))
    elif request.user.role == 'Salesman':
        return HttpResponseRedirect(reverse_lazy("salesman:dashboard"))
    else:
        logout(request)
        raise Http404

