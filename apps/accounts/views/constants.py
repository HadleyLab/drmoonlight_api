from rest_framework.response import Response
from rest_framework.decorators import api_view

from apps.accounts.models import ResidencyProgram, Speciality

@api_view()
def constants(request):
    residency_program = ResidencyProgram.objects.values('pk','name')
    speciality = Speciality.objects.values('pk','name')
    return Response(
        {
            "residency_program": residency_program,
            "speciality": speciality,
        })
