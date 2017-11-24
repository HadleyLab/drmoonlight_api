from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from apps.accounts.models import ResidencyProgram, Speciality


@api_view()
@permission_classes((AllowAny, ))
def constants(request):
    residency_program = ResidencyProgram.objects.values('pk', 'name')
    speciality = Speciality.objects.values('pk', 'name')

    return Response(
        {
            'residency_program': list(residency_program),
            'speciality': list(speciality),
        })
