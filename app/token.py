from itsdangerous import URLSafeTimedSerializer
from flask import current_app
# from this tutorial https://realpython.com/blog/python/handling-email-confirmation-in-flask/

#generate a confirmation token to send in the email
def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])
    
#confirm the token is valid
def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token, 
            salt=current_app.config['SECURITY_PASSWORD_SALT'], 
            max_age=expiration
        )
    except:
        return False
    return email
        