from rest_framework import serializers
from .models import Plan, Category
from users.models import Profile

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'color', 'is_public']

class PlanSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, required=False)

    class Meta:
        model = Plan
        fields = ['id', 'title', 'category', 'start', 'end', 'participant', 'memo']

    def create(self, validated_data):
        categories_data = validated_data.pop('cateogry', [])
        participant_data = validated_data.pop('participant', [])

        author = self.context['request'].user
        validated_data.pop('author', None)
        
        plan = Plan.objects.create(author=author, **validated_data)
        
        for category_data in categories_data:
            category, created = Category.objects.get_or_create(**category_data)
            plan.category.add(category)

        plan.participant.set(participant_data)

        return plan

    def update(self, instance, validated_data):
        categories_data = validated_data.pop('category', [])
        participant_data = validated_data.pop('participant', [])

        instance.title = validated_data.get('title', instance.title)
        instance.start = validated_data.get('start', instance.start)
        instance.end = validated_data.get('end', instance.end)
        instance.memo = validated_data.get('memo', instance.memo)
        instance.save()

        instance.category.clear()
        for category_data in categories_data:
            category, created = Category.objects.get_or_create(**category_data)
            instance.category.add(category)

        instance.participant.set(participant_data)

        return instance
