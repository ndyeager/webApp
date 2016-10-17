DEBUG = True
SECRET_KEY = 'sksjdhfihdsahfdshaksjfjsdkjfsdjdskkdfjsij'
SQLALCHEMY_DATABASE_URI = 'postgres://localhost/webApp'
SQLALCHEMY_TRACK_MODIFICATIONS = True

SECURITY_REGISTERABLE = True
SECURITY_RECOVERABLE = True
SECURITY_CHANGEABLE  = True
SECURITY_CONFIRMABLE = True


MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT =  587
MAIL_USE_SSL = False
MAIL_USE_TLS = True
MAIL_USERNAME = 'naeem@codeforprogress.org'
MAIL_PASSWORD = 'jedimindtrick'

SECURITY_EMAIL_SUBJECT_REGISTER = 'Welcome to WebApp!'
SECURITY_EMAIL_SUBJECT_PASSWORD_NOTICE = 'Your password has been reset'
SECURITY_EMAIL_SUBJECT_PASSWORD_RESET = 'Password reset instructions'
SECURITY_EMAIL_SUBJECT_PASSWORD_CHANGE_NOTICE = 'Your password has been changed'
SECURITY_EMAIL_SUBJECT_CONFIRM = 'Please confirm your email'








