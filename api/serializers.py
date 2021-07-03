from main.models import Question
from rest_framework import serializers
######################################################################
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id','author','title','body','created_at','updated_at']
