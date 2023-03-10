from rest_framework import serializers

from tracker.models import Habit
from tracker.validators import ValidateTimeToComplete, ValidateAward, ValidateAwardConnectionNull, \
    ValidatePleasantFalseOrTrue, ValidatePleasantAwardConnection, ValidateFrequency, Validate_Pleasant


class HabitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        exclude = ['user']
        validators = [
            Validate_Pleasant(field=('pleasant', 'connection')),
            ValidateTimeToComplete(field='time_to_complete'),
            ValidateAward(field=('award','connection')),
            ValidateAwardConnectionNull(field=('pleasant','connection','award')),
            ValidatePleasantFalseOrTrue(field='pleasant'),
            ValidatePleasantAwardConnection(field=('pleasant','connection','award')),
            ValidateFrequency(field='frequency')
        ]
