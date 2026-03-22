from rest_framework import serializers

class LogEntrySerializer(serializers.Serializer):
    service_name = serializers.CharField()
    level = serializers.ChoiceField(choices=["INFO", "ERROR", "WARNING", "DEBUG"])
    message = serializers.CharField()
    timestamp = serializers.DateTimeField()
    metadata = serializers.DictField(required=False)