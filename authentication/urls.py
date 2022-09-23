from django.views.decorators.csrf import csrf_exempt
from . views import EmailValidationView, RegistrationView ,CompletePasswordReset, RequestPasswordResetEmail, UsernameValidationView, VerificationView,LogoutView, LoginView
from django.urls import path
urlpatterns = [
    path('login', LoginView.as_view(), name='nlogin'),
    path('logout', LogoutView.as_view(), name='nlogout'),
    path('reg', RegistrationView.as_view(), name='nregister'),
    path('validate-username', csrf_exempt( UsernameValidationView.as_view()), name='nvalidate-username'),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()), name='nvalidate-email'),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='nactivate'),
    path('request-reset-link', RequestPasswordResetEmail.as_view(), name='nreset'),
    path('set-new-password/<uidb64>/<token>', CompletePasswordReset.as_view(), name='reset-user-password'),

]

