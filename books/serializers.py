from rest_framework import serializers
from .models import Books



class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ['title', 'author', 'status']

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("Title is required.")
        return value