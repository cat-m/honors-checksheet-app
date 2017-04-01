
class BaseConfig(object):
    
    """
    Common configurations
    """
    
    #mail config
    SECRET_KEY = 'whatever'
    SECURITY_PASSWORD_SALT = 'whatever_man'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    #gmail authentication
    MAIL_USERNAME = 'honorsprogram.test'
    MAIL_PASSWORD = 'H0norsPr0gram'
    
    #mail accounts 
    MAIL_DEFAULT_SENDER = 'honorsprogram.test@gmail.com'
    
    
class DevelopmentConfig(BaseConfig):
    
    """
    Development configurations
    """
    
    DEBUG = True
    SQLALCHEMY_ECHO = True

    
class ProductionConfig(BaseConfig):
    
    """
    Production configurations
    """
    
    DEBUG = False
    
app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}