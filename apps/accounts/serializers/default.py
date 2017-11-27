from rest_framework import serializers


class CurrentUserResidentDefault(serializers.CurrentUserDefault):
    def __call__(self):
        return self.user.resident


class CurrentUserSchedulerDefault(serializers.CurrentUserDefault):
    def __call__(self):
        return self.user.scheduler
