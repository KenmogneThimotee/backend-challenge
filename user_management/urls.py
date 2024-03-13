
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .views import CustumObtainTokenPairView, RegisterView



urlpatterns = [
    path('login', CustumObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup', RegisterView.as_view(), name='auth_register'),
]
