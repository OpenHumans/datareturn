from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from datareturn.views import UserTokensView

urlpatterns = [
    url(r'^admin/user_tokens', UserTokensView.as_view(), name='admin_user_tokens'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', TemplateView.as_view(template_name='datareturn/home.html'), name='home'),
    url(r'^account/', include('allauth.urls')),
]
