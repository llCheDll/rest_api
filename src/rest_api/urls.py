from django.conf.urls import url, include

from rest_api.views import PostViewSet, RegisterView

from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)


router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^signup/$', RegisterView.as_view(), name='register'),
    url(r'^login/$', TokenObtainPairView.as_view(), name='login'),
]
