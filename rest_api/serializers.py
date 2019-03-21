from rest_framework import serializers
from rest_api.models import Post
from django.contrib.auth.models import User


class PostSerializer(serializers.ModelSerializer):
    likes_counter = serializers.SerializerMethodField()
    liked_by = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'content',
            'author',
            'slug',
            'likes_counter',
            'liked_by'
        )
        lookup_field = 'id'

    def get_likes_counter(self, obj):
        return obj.like.count()

    def get_liked_by(self, obj):
        return obj.like.values('username')


class RegisterSerializer(serializers.Serializer):
    username_field = User.USERNAME_FIELD

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'] = serializers.EmailField()
        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = serializers.CharField(
            style={'input_type': 'password'}
        )
        self.fields['password_repeat'] = serializers.CharField(
            style={'input_type': 'password'}
        )

    def create(self, validated_data):
        email = self.validated_data['email']
        username = self.validated_data[self.username_field]
        password = self.validated_data['password']

        user = User(username=username, email=email, password=password)
        user.set_password(user.password)
        user.save()

        return user