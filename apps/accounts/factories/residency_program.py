from factory import DjangoModelFactory

from apps.accounts.models import ResidencyProgram


class ResidencyProgramFactory(DjangoModelFactory):

    class Meta:
        model = ResidencyProgram
