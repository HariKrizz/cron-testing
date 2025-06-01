from rest_framework import serializers

from .models import Student
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'date_of_birth']

    def validate_first_name(self, value):
        if not value:
            raise serializers.ValidationError("First name is required.")
        return value


class StudentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'status']

    def validate_first_name(self, value):
        if not value:
            raise serializers.ValidationError("First name is required.")
        return value
    