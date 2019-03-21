from rest_framework_simplejwt.authentication import AUTH_HEADER_TYPES, JWTAuthentication
from rest_framework import generics
from rest_framework import viewsets
from rest_api.models import Post
from rest_api.serializers import PostSerializer, RegisterSerializer
from rest_framework.response import Response
from rest_framework import status

class RegisterView(generics.GenericAPIView):
    permission_classes = ()
    authentication_classes = (JWTAuthentication,)

    serializer_class = RegisterSerializer

    www_authenticate_realm = 'api'

    def get_authenticate_header(self, request):
        return '{0} realm="{1}"'.format(
            AUTH_HEADER_TYPES[0],
            self.www_authenticate_realm,
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response({'status': 'user_create'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request):
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'post_create'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)




