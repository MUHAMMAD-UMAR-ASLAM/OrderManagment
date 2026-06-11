from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import CreateUserView

urlpatterns = [
    path('login/',TokenObtainPairView.as_view(),name='login'),
    path('refresh/',TokenRefreshView.as_view(),name='refresh'),

    path('signup',CreateUserView.as_view(),name='signup'),
]