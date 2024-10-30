from rest_framework import serializers
from .models import Plan, Category
from users.models import Profile

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'color', 'is_public']

class PlanSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Plan
        fields = ['id', 'title', 'category', 'start', 'end', 'participant', 'memo']

    def create(self, validated_data):
        validated_data.pop('author', None)
        author = self.context['request'].user
        participant_data = validated_data.pop('participant', [])
        
        plan = Plan.objects.create(author=author, **validated_data)
        plan.participant.set(participant_data)
        return plan

    def update(self, instance, validated_data):
        participant_data = validated_data.pop('participant', [])

        instance.title = validated_data.get('title', instance.title)
        instance.start = validated_data.get('start', instance.start)
        instance.end = validated_data.get('end', instance.end)
        instance.memo = validated_data.get('memo', instance.memo)

        instance.participant.set(participant_data)
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.category:
            representation['category'] = CategorySerializer(instance.category).data
        return representation