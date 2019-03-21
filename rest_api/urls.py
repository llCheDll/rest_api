from django.conf.urls import url, include
from rest_framework import routers
from rest_api.views import PostViewSet, RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^register/$', RegisterView.as_view(), name='register' ),
    url(r'^login/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^token/refresh/$', TokenRefreshView.as_view(), name='token_refresh')
    # url(r'posts/<int:pk>/like/', PostViewSet.like)
]

