from django.urls import path
from account.views.account import PasswordChangeView, UpdateTwoFactorAuthenticationView, UserProfileView
from account.views.auth import PasswordResetConfirmView, PasswordResetRequestView

urlpatterns = [

    path('', UserProfileView.as_view()),
    path('change-password/', PasswordChangeView.as_view(), name='password-change'),
    path('reset-password', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('reset-password/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('two-factor', UpdateTwoFactorAuthenticationView.as_view(), name='UpdateTwoFactorAuthenticationView'),
]
