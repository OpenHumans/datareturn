import csv
import datetime
import json

from allauth.account.utils import user_pk_to_url_str, url_str_to_user_pk

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.generic import RedirectView, TemplateView, View

import requests

from datareturn.models import DataFile, OpenHumansUser

User = get_user_model()


class TokenLoginView(View):
    """
    Log in a user using the reset token as authentication.

    Tokens are invalidated after being used, and expire after 3 days.
    (Expiration time can be altered with settings.PASSWORD_RESET_TIMEOUT_DAYS.)
    """

    def _get_user(self, uidb36):
        try:
            pk = url_str_to_user_pk(uidb36)

            return User.objects.get(pk=pk)
        except (ValueError, User.DoesNotExist):
            return None

    def dispatch(self, request, *args, **kwargs):
        uidb36 = kwargs['uidb36']
        token = kwargs['token']
        self.reset_user = self._get_user(uidb36)
        user = authenticate(username=self.reset_user, token=token)
        if user:
            login(request, user)
            login_url = reverse('home')
            return HttpResponseRedirect(login_url)
        failed_login_url = reverse('token_login_fail')
        return HttpResponseRedirect(failed_login_url)


class UserTokensView(TemplateView):
    """
    Link to a CSV containing user emails and freshly generated tokens.
    """
    template_name = 'admin/user_tokens.html'

    @method_decorator(staff_member_required)
    def get(self, request, *args, **kwargs):
        return super(UserTokensView, self).get(request, *args, **kwargs)


class UserTokensCSVView(View):
    """
    Return a CSV containing user emails and freshly generated tokens.
    """

    def get_user_tokens(self):
        users_with_data = []
        for data_file in DataFile.objects.all():
            if data_file.user not in users_with_data:
                users_with_data.append(data_file.user)
        users_and_tokens = []
        for user in users_with_data:
            token = default_token_generator.make_token(user)
            login_path = reverse('token_login',
                                 kwargs={'uidb36': user_pk_to_url_str(user),
                                         'token': token})
            login_url = self.request.build_absolute_uri(login_path)
            users_and_tokens.append([user, login_url])
        return users_and_tokens

    @method_decorator(staff_member_required)
    def get(self, request, *args, **kwargs):
        """
        Return CSV file. Lists users (emails) and a fresh set of login tokens.

        The resulting file is named "datareturn_user_tokens_{DATETIME}.csv"
        where the [DATETIME] section is date and time in ISO 8601 basic format.
        """
        # Add the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        datetimestamp = datetime.datetime.now().strftime('%y%m%dT%H%m%S')
        response['Content-Disposition'] = (
            'attachment; filename="datareturn_user_tokens_{}.csv"'.format(
                datetimestamp))
        writer = csv.writer(response)
        users_and_tokens = self.get_user_tokens()
        for user, token in users_and_tokens:
            writer.writerow([user.email, token])

        return response


class AuthorizeOpenHumansView(RedirectView):
    pattern_name = 'home'

    @staticmethod
    def _exchange_code(code):
        site = Site.objects.get_current()

        token_response = requests.post(
            site.openhumansconfig.token_url,
            data={
                'code': code,
                'client_id': settings.OPEN_HUMANS_CLIENT_ID,
                'client_secret': settings.OPEN_HUMANS_CLIENT_SECRET,
                'grant_type': 'authorization_code',
                'redirect_uri': settings.OPEN_HUMANS_REDIRECT_URI,
            })

        return token_response.json()

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        if 'code' in request.GET:
            token_data = self._exchange_code(request.GET['code'])

            ohuser, _ = OpenHumansUser.objects.get_or_create(user=request.user)

            ohuser.access_token = token_data['access_token']
            ohuser.refresh_token = token_data['refresh_token']
            ohuser.token_expiration = (
                timezone.now() +
                datetime.timedelta(seconds=token_data['expires_in']))

            ohuser.save()

            site = Site.objects.get_current()
            requests.patch(
                site.openhumansconfig.userdata_url,
                data=json.dumps({
                    'data': ohuser.create_exported_data(),
                }),
                headers={'Content-type': 'application/json',
                         'Authorization':
                         'Bearer {}'.format(ohuser.get_access_token())})

            site = Site.objects.get_current()

            messages.success(request, 'Open Humans connection completed.')

            return HttpResponseRedirect(site.openhumansconfig.return_url)

        messages.error(request, 'Failed to connect Open Humans!')

        return super(AuthorizeOpenHumansView, self).get(
            request, *args, **kwargs)
