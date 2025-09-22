from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.db.models import Q

class EmailMobileBackend(BaseBackend):
    """
    Custom authentication backend that allows users to login with email or mobile number
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None
            
        try:
            # Try to find user by username, email, or mobile number
            user = User.objects.get(
                Q(username=username) | 
                Q(email=username) |
                Q(client_profile__mobile=username)
            )
            
            # Check password
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
                
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user
            User().set_password(password)
            return None
        
        return None
    
    def user_can_authenticate(self, user):
        """
        Reject users with is_active=False. Custom user models that don't have
        is_active field are allowed.
        """
        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None