from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from datareturn.views import (HomeView, TokenLoginView, UserTokensView,
                              UserTokensCSVView)

urlpatterns = [
    url(r'^admin/user_tokens/?$', UserTokensView.as_view(),
        name='admin_user_tokens'),
    url(r'^admin/user_tokens_csv/?$', UserTokensCSVView.as_view(),
        name='admin_user_tokens_csv'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$',
        TemplateView.as_view(template_name='datareturn/home.html'),
        # HomeView.as_view(),
        name='home'),
    url(r'^account/', include('allauth.urls')),
    url(r"^token_login/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$",
        TokenLoginView.as_view(), name='token_login'),
    url(r'^token_login_fail/?$',
        TemplateView.as_view(template_name='datareturn/token_login_fail.html'),
        name='token_login_fail'),
]
