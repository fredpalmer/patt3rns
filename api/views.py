from patt3rns.models import Pattern, Participant, Action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, serializers, generics, mixins, status, viewsets


# class PatternList(generics.ListCreateAPIView):
# permission_classes = (permissions.IsAuthenticated, )
#     queryset = Pattern.objects.all()

class BaseMeta(object):
    exclude = ("uuid", "date_created", "date_modified", )


class ActionSerializer(serializers.ModelSerializer):
    class Meta(BaseMeta):
        model = Action


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta(BaseMeta):
        model = Participant


class PatternModelSerializer(serializers.ModelSerializer):
    participant = ParticipantSerializer()
    action = ActionSerializer()

    class Meta(BaseMeta):
        model = Pattern
        # fields = ()
        depth = 2
        exclude = ("edited_by", "uuid", "date_created", "date_modified", )


class PatternViewSet(viewsets.ModelViewSet):
    model = Pattern
    serializer_class = PatternModelSerializer
    # queryset = Pattern.objects.all()
