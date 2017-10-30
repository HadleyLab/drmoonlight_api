from factory import DjangoModelFactory, fuzzy

from apps.accounts.models import ResidencyProgram


class ResidencyProgramFactory(DjangoModelFactory):
    name = fuzzy.FuzzyText()

    class Meta:
        model = ResidencyProgram
