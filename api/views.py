from main.models import Question
from .serializers import QuestionSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics,status
################################################################
@api_view(['GET'])
def QuestionView(request):
    api_urls = {
        'List': '/question-list/',
        'Post': '/question-list-top-five/',
    }
    return Response(api_urls)
################################################################
@api_view(['GET'])
def questionlist(request):
    questiones = Question.objects.all()
    serializer = QuestionSerializer(questiones, many=True)
    return Response(serializer.data)

##################################################################
@api_view(['GET'])
def questionlisttopfive(request,text_to_search):
    searchQuery = text_to_search.split("search_query=")[1].lower().replace("+"," ")
    print(searchQuery)
    questiones = Question.objects.filter(title__icontains=searchQuery).order_by("-created_at")[:5]
    serializer = QuestionSerializer(questiones, many=True)
    print(len(serializer.data))
    return Response(serializer.data)
