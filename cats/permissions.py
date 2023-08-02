# базовый класс с доступами:

# class BasePermission(metaclass=BasePermissionMetaclass):

#     # Определяет права на уровне запроса и пользователя
#     def has_permission(self, request, view):
#         return True

#     # Определяет права на уровне объекта
#     def has_object_permission(self, request, view, obj):
#         return True 


from rest_framework import permissions

class OwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS # Если метод запроса безопасный (то есть GET, HEAD или OPTIONS)
                or request.user.is_authenticated # или если пользователь аутентифицирован 
            ) # возвращаем true
        
    # Если has_permission() вернул True, то после получения объекта вызывается метод has_object_permission() (Если оплучили список, то has_object_permission не вызывается)
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user # если пользователь - создатель объекта, то True (!) анонимный пользователь не увидит информацию об одном объекте

# чтоб аноним мог посмотреть инф об одном объекте создадим:
class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS 