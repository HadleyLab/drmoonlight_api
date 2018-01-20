from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from apps.accounts.models import (
    Speciality, US_STATES, TIMEZONES)


@api_view()
@permission_classes((AllowAny, ))
def constants(request):
    speciality = Speciality.objects.values('pk', 'name')

    return Response(
        {
            'speciality': list(speciality),
            'us_states': [
                {'pk': key, 'name': value} for key, value in US_STATES
            ],
            'timezones': [
                {'pk': key, 'name': value} for key, value in TIMEZONES
            ],
        })
