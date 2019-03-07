from rest_framework import serializers
from .models import Testing, MatchTask, MultiChoiceQuestion, Choice, MatchQuestion,  TFStatement, WordBoxTask, Sentence


class WBSentenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sentence
        fields = ('question_text', 'choice', 'points')


class WBserializer(serializers.ModelSerializer):
    sentences = WBSentenceSerializer(many=True, read_only=True)

    class Meta:
        model = WordBoxTask
        fields = ('task_name', 'without_wordbox', 'sentences')


class TFStatSerializer(serializers.ModelSerializer):

    class Meta:
        model = TFStatement
        fields = ('statement', 'True?')


# class TFTaskSerializer(serializers.ModelSerializer):
#     tf_stats = TFStatSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = TFTask
#         fields = ('task_name', 'tf_stats')


class MatchQuestionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = MatchQuestion
        fields = ('question_text', 'choice', 'points')


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('choice_text', 'points')


class MatchSerializer(serializers.ModelSerializer):
    match_options = MatchQuestionsSerializer(many=True, read_only=True)

    class Meta:
        model = MatchTask
        fields = ('task', 'match_task_name', 'match_options')


class MultiChoiceSerializer(serializers.ModelSerializer):
    multis_choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = MultiChoiceQuestion
        fields = ('task', 'question', 'multis_choices')


class TestingSerializer(serializers.ModelSerializer):
    matches = MatchSerializer(many=True, read_only=True)
    multis = MultiChoiceSerializer(many=True, read_only=True)
    tf_tasks = TFStatSerializer(many=True, read_only=True)
    word_boxes = WBserializer(many=True, read_only=True)

    class Meta:
        model = Testing
        fields = ('id', 'test_name', 'all_time_opened', 'test_opening_date', 'test_closing_date', 'description',
                   'matches', 'multis', 'tf_tasks', 'word_boxes')




