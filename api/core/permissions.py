from rest_framework.permissions import BasePermission

class IsStaffOrRelated(BasePermission):
    """
    Custom permission to allow only staff members or related users to view, but only staff can edit.
    """
    def has_permission(self, request, view):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user.is_staff
        return True

    def has_object_permission(self, request, view, obj):
        # Allow staff full access
        if request.user.is_staff:
            return True

        # Otherwise, allow only viewing (GET) and ensure the user is related to the transaction
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return (
                (hasattr(obj, 'sender_account') and obj.sender_account.owner == request.user) or
                (hasattr(obj, 'recipient_account') and obj.recipient_account.owner == request.user)
            )
        return False

