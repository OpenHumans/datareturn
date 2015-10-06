from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from datareturn.views import TokenLoginView, UserTokensView

urlpatterns = [
    url(r'^admin/user_tokens', UserTokensView.as_view(), name='admin_user_tokens'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', TemplateView.as_view(template_name='datareturn/home.html'), name='home'),
    url(r'^account/', include('allauth.urls')),
    url(r'^token_login/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        TokenLoginView.as_view(), name='token_login'),
]
