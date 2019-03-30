from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .exceptions import UserExistsException
from rest_api.models import Post
from rest_api.serializers import PostSerializer, RegisterSerializer
from django.contrib.auth.models import User


class RegisterView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        try:
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'user_create'})
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        except UserExistsException:
            return Response(
                {'status': 'user_exists'},
                status=status.HTTP_400_BAD_REQUEST
            )


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        post = Post.objects.get(id=pk)
        response_data = {'status': None}

        if request.user in User.objects.all():
            if 'action' in request.data:
                if request.data['action'] == 'unlike':
                    post.like.remove(request.user.id)
                    response_data['status'] = request.data['action']

                    return Response(response_data)
                if request.data['action'] == 'like':
                    post.like.add(request.user.id)
                    response_data['status'] = request.data['action']

                    return Response(response_data)
        return Response(
            {'status': 'bad request'},
            status=status.HTTP_400_BAD_REQUEST
        )
