from rest_framework import serializers
from .models import Test, Student


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['test_name', 'points_for_test']


class StudSerializer(serializers.ModelSerializer):
    tests = TestSerializer(many=True, read_only=False)

    class Meta:
        model = Student
        fields = ['id', 'name', 'telegram_username', 'telegram_id', 'tests']

    def create(self, validated_data):
        test_data = validated_data.pop('tests')
        student = Student.objects.create(**validated_data)
        for i in test_data:
            Test.objects.create(stud_id=student.id, **i)

        return student

    def update(self, instance, validated_data):
        tests = validated_data.pop('tests')

        instance.name = validated_data.get('name', instance.name)
        instance.telegram_username = validated_data.get('telegram_username', instance.name)
        instance.save()
        for test in tests:
            Test.objects.all().update_or_create(stud_id=instance.id,**test)
        return instance

