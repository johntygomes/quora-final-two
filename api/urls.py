from django.urls import path
from .views import QuestionView, questionlist, questionlisttopfive


urlpatterns = [
    path('', QuestionView, name='QuestionView'),
    path('question-list/', questionlist, name='question-list'),
    path('question-list-top-five/<text_to_search>', questionlisttopfive, name='question-list-top-five'),
]