from rest_framework.permissions import BasePermission

class IsStaffOrRelated(BasePermission):
    """
    Custom permission to allow only staff members or related users to view, but only staff can edit.
    """
    # List of view basename names where staff-only creation applies
    BASE_NAMES = ['account']

    def has_permission(self, request, view):
        # Allow POST requests for staff and related users if the view is related to Transaction
        if request.method == 'POST' and view.basename in self.BASE_NAMES:
            return request.user.is_staff

        # Allow PUT, PATCH, DELETE requests for staff only
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user.is_staff

        # Allow other methods (GET, HEAD, OPTIONS) for all users
        return True

    def has_object_permission(self, request, view, obj):
        # Allow staff full access
        if request.user.is_staff:
            return True

        # Otherwise, allow only viewing (GET) and ensure the user is related to the transaction
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return (
                ((hasattr(obj, 'sender_account') and obj.sender_account.owner == request.user)) or
                ((hasattr(obj, 'recipient_account') and obj.recipient_account.owner == request.user)) or
                ((hasattr(obj, 'owner') and obj.owner == request.user))
            )
        return False

