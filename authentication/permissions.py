from rest_framework.permissions import BasePermission

class HasModulePermission(BasePermission):
    """
    Foydalanuvchining roliga qarab CRUD huquqlarini tekshiruvchi global klass
    """
    def has_permission(self, request, view):
        # Agar superuser bo'lsa, hamma narsaga ruxsat
        if request.user.is_superuser:
            return True
            
        # Agar foydalanuvchiga rol biriktirilmagan bo'lsa, ruxsat bermaymiz
        if not request.user.role or not request.user.role.is_active:
            return False
            
        role = request.user.role
        
        # Mahsulotlar (Products) moduli uchun tekshirish
        if view.basename == 'product':
            if request.method == 'GET':
                return role.can_view_products
            elif request.method == 'POST':
                return role.can_create_products
            elif request.method in ['PUT', 'PATCH']:
                return role.can_edit_products
            elif request.method == 'DELETE':
                return role.can_delete_products
                
        # Savdolar (Sales) moduli uchun tekshirish
        if view.basename == 'sale':
            if request.method == 'GET':
                return role.can_view_sales
            elif request.method == 'DELETE':
                return role.can_delete_sales
                
        return False