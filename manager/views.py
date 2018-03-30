from django.shortcuts import render
from login.decorators import check_role
from django.views.generic.base import View
from django.utils.decorators import method_decorator
# Create your views here.


@method_decorator(check_role('Manager'), name='dispatch')
class Dashboard(View):
    template_name = 'manager/dashboard.html'

    def get(self, request, *args, **kwargs):
        template = self.template_name
        return render(request, template)




