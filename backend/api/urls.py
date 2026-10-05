from django.urls import path
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # POST {"email", "password"} -> {"access", "refresh"}
    path('auth/login/', TokenObtainPairView.as_view(), name='auth-login'),
    # POST {"refresh"} -> {"access", "refresh"} (refresh cũ bị vô hiệu)
    path('auth/refresh/', TokenRefreshView.as_view(), name='auth-refresh'),
    # POST {"refresh"} -> đăng xuất (đưa refresh token vào blacklist)
    path('auth/logout/', TokenBlacklistView.as_view(), name='auth-logout'),
]
