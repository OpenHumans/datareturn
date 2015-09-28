import csv
import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import View

from datareturn.models import DataFile

User = get_user_model()


class UserTokensView(View):

    def get_user_tokens(self):
        users_with_data = []
        for data_file in DataFile.objects.all():
            if data_file.user not in users_with_data:
                users_with_data.append(data_file.user)
        users_and_tokens = []
        for user in users_with_data:
            token = default_token_generator.make_token(user)
            users_and_tokens.append([user, token])
        return users_and_tokens

    @method_decorator(staff_member_required)
    def get(self, request, *args, **kwargs):
        # Create the HttpResponse object with the appropriate CSV header.
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
