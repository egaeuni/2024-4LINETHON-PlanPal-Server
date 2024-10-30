from rest_framework import serializers
from .models import Plan, Category
from users.models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'color', 'is_public']

class PlanSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='title', queryset=Category.objects.all(), allow_null=True, required=False)
    participant = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all(), many=True, required=False)

    class Meta:
        model = Plan
        fields = ['id', 'title', 'category', 'start', 'end', 'participant', 'memo']

    def create(self, validated_data):
        validated_data.pop('author', None)
        author = self.context['request'].user
        participant_data = validated_data.pop('participant', [])
        
        category_title = validated_data.pop('category', None)
        if category_title:
            category, created = Category.objects.get_or_create(title=category_title)
            validated_data['category'] = category

        plan = Plan.objects.create(author=author, **validated_data)
        plan.participant.set(participant_data)
        return plan

    def update(self, instance, validated_data):
        participant_data = validated_data.pop('participant', [])
        category_title = validated_data.pop('category', None)

        if category_title is not None:
            category, created = Category.objects.get_or_create(title=category_title)
            instance.category = category

        instance.title = validated_data.get('title', instance.title)
        instance.start = validated_data.get('start', instance.start)
        instance.end = validated_data.get('end', instance.end)
        instance.memo = validated_data.get('memo', instance.memo)

        if category is not None:
            instance.category = category

        instance.participant.set(participant_data)
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.category:
            representation['category'] = CategorySerializer(instance.category).data
        representation['participant'] = [user.username for user in instance.participant.all()]
        return representation