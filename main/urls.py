from django.urls import path
from . import views

urlpatterns = [
    path('register', views.registerPage, name='register'),
    path('email-verified', views.emailverified, name='email-verified'),
    path('email-verification-failed', views.emailverificationfailed, name='email-verification-failed'),
    path('login', views.loginPage, name='login'),
    path('login-new', views.loginNew, name='login-new'),
    path('register-new', views.registerNew, name='register-new'),
    path('logout-new', views.logoutPage, name='logout-new'),
    path('', views.homePage, name='index'),
    path('new-question', views.newQuestionPage, name='new-question'),
    path('question/<int:id>', views.questionPage, name='question'),
    path('reply', views.replyPage, name='reply'),
]
