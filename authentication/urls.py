from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # Router ichidagi avtomatik URL-lar (roles/ va users/)
    path('', include(router.urls)),
    
    # 🎯 MANA SHU QATORNI QO'SHAMIZ:
    # Endi login so'rovi to'g'ridan-to'g'ri shu yerga keladi
    path('web-login/', WebLoginView.as_view(), name='web_login'),
    path('me/', current_user, name='current_user'),
    path('change-password/', change_password, name='change_password'),
]