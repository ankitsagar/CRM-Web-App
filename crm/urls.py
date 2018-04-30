"""crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView


from login.views import verify_login
# from customer.views import CustomerListView, CustomerDetailView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', RedirectView.as_view(url=reverse_lazy('account_login'))),
    url(r'^accounts/login/$', RedirectView.as_view(url=reverse_lazy('account_login'))),
    url(r'^signup/$', RedirectView.as_view(url=reverse_lazy('account_login'))),
    url(r'^verify-login/$', verify_login, name='verify-login'),
    url(r'^', include('allauth.urls')),

    url(r'^manager/', include('manager.urls', namespace='manager')),
    url(r'^salesman/', include('salesman.urls', namespace='salesman')),
    url(r'^customer/', include('customer.urls', namespace='customer')),


    # url(r'^(?P<pk>\d+)/$', CustomerDetailView.as_view(), name="customer_detail"),
    # url(r'^$', CustomerListView.as_view(), name="customer_list"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
