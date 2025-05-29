class Config:
    SECRET_KEY = "super-secret-key"  # Change this in production
    SQLALCHEMY_DATABASE_URI = "sqlite:///chatbot.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT = "salty"  # Change this in production
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_LOGIN_USER_TEMPLATE = 'security/login.html'
    SECURITY_REGISTER_USER_TEMPLATE = 'security/register.html'
    SECURITY_POST_LOGIN_VIEW = '/'
    SECURITY_POST_REGISTER_VIEW = '/'
    SECURITY_POST_LOGOUT_VIEW = '/login'
