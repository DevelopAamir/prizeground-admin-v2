from rest_framework import authentication, exceptions
import firebase_admin.auth
from django.contrib.auth.models import User
from api.models import FirebaseUser

def save_firebase_user(user, display_name, email, email_verified, photo_url):
    user, created = FirebaseUser.objects.get_or_create(user=user)
    user.display_name = display_name
    user.email = email
    user.email_verified = email_verified
    user.photo_url = photo_url
    user.save()

class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
       
        if not auth_header:
            return None
        token = auth_header.split(' ').pop()
        if not token:
            raise exceptions.AuthenticationFailed('Invalid token header. No credentials provided.')
        
        try:
            decoded_token = firebase_admin.auth.verify_id_token(token)
        except Exception as e:
            print(f"Token verification failed: {e}")
            raise exceptions.AuthenticationFailed('Invalid Firebase token.')

        uid = decoded_token.get('uid')
        
        if not uid:
            raise exceptions.AuthenticationFailed('Invalid token header. No UID provided.')

        # Get or create the user based on the Firebase UID
        user, created = User.objects.get_or_create(username=uid)
        if created:
            user.email = decoded_token.get('email')
            user.first_name = decoded_token.get('name')
            user.save()
            save_firebase_user(user, decoded_token.get('name'), decoded_token.get('email'), decoded_token.get('email_verified'),  decoded_token.get('picture'))
        return (user, None)
