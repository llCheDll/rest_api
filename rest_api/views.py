from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .exceptions import UserExistsException
from rest_api.models import Post
from rest_api.serializers import PostSerializer, RegisterSerializer


class RegisterView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            if serializer.is_valid():
                user = serializer.save()
                return Response({'status': 'user_create'})
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        except UserExistsException:
            return Response({'status': 'user_exists'}, status=status.HTTP_400_BAD_REQUEST)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'post_create'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


