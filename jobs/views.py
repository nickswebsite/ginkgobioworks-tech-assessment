from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.serializers import HyperlinkedModelSerializer

from jobs.models import Job


class JobSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Job
        fields = [
            "url",
            "created_on",
            "ended_on",
            "state",
            "current",
            "total",
            "description",
            "message",
        ]


class JobViewSet(ReadOnlyModelViewSet):
    """
    Returns a list of jobs for the current user.
    """
    queryset = Job.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = JobSerializer

    def get_queryset(self):
        return self.queryset.all()
