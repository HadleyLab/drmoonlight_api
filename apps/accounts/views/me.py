from rest_framework import generics, response, permissions

from apps.accounts.serializers import UserSerializer


class MeView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        return self.request.user

    def get(self, request):
        user = self.get_object()
        serializer = self.get_serializer(user)

        return response.Response(data=serializer.data)
