from rest_framework import viewsets, serializers
from .models import Task, Label
from user_management.models import User


class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault(), required=False)

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'created_at', 'updated_at', 'priority', 'created_by')
        read_only_fields = ('created_at', 'updated_at')
        extra_kwargs = {
            'title': {'required': True, 'error_messages': {'required': 'Title field is required.'}},
        }

    def create(self, validated_data):
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.save()
        return instance


class LabelSerializer(serializers.ModelSerializer):
    
    created_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
        required=False
    )
    
    # def get_validation_exclusions(self):
    #     exclusions = super(LabelSerializer, self).get_validation_exclusions()
    #     return exclusions + ['created_by']
    
    def __init__(self, *args, **kwargs):
        """
        Initialize the LabelSerializer object and add a 'tasks' field to the serializer's fields.
        The 'tasks' field is a PrimaryKeyRelatedField that filters the queryset based on the current user's 'created_by' field.
        """
        super().__init__(*args, **kwargs)
        user = self.context['request'].user
        self.fields['tasks'] = serializers.PrimaryKeyRelatedField(
            queryset=Task.objects.filter(created_by=user),
            many=True,
            required=False
        )
    
    class Meta:
        model = Label
        fields = ('id', 'name', 'created_by', 'tasks')
        # extra_kwargs = {"created_by": {"required": False, "allow_null": False}}

    