from rest_framework import serializers
from .models import Plan, Category
from users.models import Profile
from django.shortcuts import get_object_or_404

from promise.serializers import ProfileSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'color', 'is_public']

class PlanSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    participant = ProfileSerializer(many=True, read_only=True)
    is_completed = serializers.BooleanField(required=False)

    class Meta:
        model = Plan
        fields = ['id', 'title', 'category', 'start', 'end', 'participant', 'memo', 'is_completed']
        read_only_fields = ['author']

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     if instance.category:
    #         representation['category'] = CategorySerializer(instance.category).data
    #     representation['participant'] = [user.username for user in instance.participant.all()]
    #     return representation