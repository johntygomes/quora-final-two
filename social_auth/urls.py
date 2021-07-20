from django.urls import path
from .views import GoogleSocialAuthView,logoutGoogleView

urlpatterns=[
    path('google/', GoogleSocialAuthView.as_view()),
    path('logout-google/', logoutGoogleView),
    # path('facebook/', FacebookSocialAuthView.as_view()),
    # path('twitter/', TwitterSocialAuthView.as_view()),
]