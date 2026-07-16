from rest_framework import viewsets
from .models import User, Role
from .serializers import UserSerializer, RoleSerializer
from rest_framework.permissions import IsAuthenticated
# authentication/views.py (yoki mos keladigan login view faylida)
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import authenticate, login, logout


class WebLoginView(APIView):
    def post(self, request):
        login_input = request.data.get('username') or request.data.get('phone')
        password = request.data.get('password')
        client = request.data.get('client', 'web')  # 'web' yoki 'desktop'

        user = authenticate(username=login_input, password=password)

        if user is not None:
            login(request, user)
            is_admin = user.is_superuser or (user.role and user.role.name == "Admin")

            # 🆕 Desktop dastur faqat Cashier uchun — Admin bo'lsa, sessiyani darhol yopamiz
            if client == 'desktop' and is_admin:
                logout(request)
                return Response({
                    "success": False,
                    "error": "Bu dastur faqat kassirlar uchun mo'ljallangan!"
                }, status=status.HTTP_403_FORBIDDEN)

            if is_admin:
                return Response({
                    "success": True,
                    "redirect_to": "/dashboard/",
                    "role": "admin",
                    "message": "Xush kelibsiz, Admin!"
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "success": True,
                    "redirect_to": "/pos/",
                    "role": "cashier",
                    "message": "Smena oynasiga yo'naltirilmoqda..."
                }, status=status.HTTP_200_OK)

        return Response({
            "success": False,
            "error": "Login yoki parol xato!"
        }, status=status.HTTP_400_BAD_REQUEST)


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all().order_by('id')
    serializer_class = RoleSerializer

    def destroy(self, request, *args, **kwargs):
        role = self.get_object()
        if role.is_system:
            return Response({"error": "Tizim rolini o'chirib bo'lmaydi!"}, status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]
    
    
    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        """Parolni yangilash: POST /api/auth/users/{id}/set_password/  { password }"""
        user = self.get_object()
        password = request.data.get('password', '')
        if len(password) < 6:
            return Response({"error": "Parol kamida 6 belgidan iborat bo'lishi kerak!"}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(password)
        user.save()
        return Response({"success": True, "message": "Parol muvaffaqiyatli yangilandi"})


@api_view(['GET'])
def current_user(request):
    """Joriy tizimga kirgan foydalanuvchi: GET /api/auth/me/"""
    if request.user.is_authenticated:
        return Response({"id": request.user.id, "username": request.user.username})
    return Response({"id": None, "username": None})





@api_view(['POST'])
def change_password(request):
    """ POST /api/auth/change-password/ { current_password, new_password, confirm_password } """
    if not request.user.is_authenticated:
        return Response({"error": "Tizimga kirilmagan"}, status=status.HTTP_401_UNAUTHORIZED)

    current_password = request.data.get('current_password', '')
    new_password = request.data.get('new_password', '')
    confirm_password = request.data.get('confirm_password', '')

    if not request.user.check_password(current_password):
        return Response({"error": "Joriy parol noto'g'ri!"}, status=status.HTTP_400_BAD_REQUEST)

    if len(new_password) < 6:
        return Response({"error": "Yangi parol kamida 6 belgidan iborat bo'lishi kerak!"}, status=status.HTTP_400_BAD_REQUEST)

    if new_password != confirm_password:
        return Response({"error": "Yangi parollar mos kelmadi!"}, status=status.HTTP_400_BAD_REQUEST)

    request.user.set_password(new_password)
    request.user.save()
    update_session_auth_hash(request, request.user)  # Sessiyani uzmasdan yangilaydi

    return Response({"success": True, "message": "Parol muvaffaqiyatli yangilandi"})