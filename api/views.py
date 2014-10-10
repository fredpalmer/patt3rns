from rest_framework import serializers, viewsets

from organization import models as organization_models


class BaseMeta(object):
    exclude = ("uuid", "date_created", "date_modified", )


class ActionSerializer(serializers.ModelSerializer):
    class Meta(BaseMeta):
        model = organization_models.Action


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta(BaseMeta):
        model = organization_models.Participant


class PatternModelSerializer(serializers.ModelSerializer):
    participant = ParticipantSerializer()
    action = ActionSerializer()

    class Meta(BaseMeta):
        model = organization_models.Pattern
        # fields = ()
        depth = 2
        exclude = ("edited_by", "uuid", "date_created", "date_modified", )


class PatternViewSet(viewsets.ModelViewSet):
    model = organization_models.Pattern
    serializer_class = PatternModelSerializer
    # queryset = Pattern.objects.all()
