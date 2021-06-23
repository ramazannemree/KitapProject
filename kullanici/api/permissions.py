from rest_framework.permissions import BasePermission,IsAdminUser

class NotAuthenticated(BasePermission):

    message = "Zaten bir hesabınız var"
    def has_permission(self, request, view):
        if view.action=="create":
            return not request.user or not request.user.is_authenticated
        elif view.action == "list":
            return False
        elif view.action in ["retrieve","update"]:
           return request.user.is_authenticated
    # def has_object_permission(self, request, view, obj):
    #     if view.action in ["retrieve","update","partial_update"]:
    #         return obj.user == request.user or IsAdminUser




class IsOwner(BasePermission):
    message = "Başkasının Profilini Görüntüleyemezsiniz"
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user