from .resident import (
    ResidentSerializer, ResidentCreateSerializer, ResidentUpdateSerializer,
    ResidentFillProfileSerializer)
from .scheduler import (
    SchedulerSerializer, SchedulerCreateSerializer, SchedulerUpdateSerializer)
from .user import UserSerializer
from .default import CurrentUserResidentDefault, CurrentUserSchedulerDefault
