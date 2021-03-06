from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.serializers import HyperlinkedModelSerializer

from jobs.models import Job


class JobSerializer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name="job-detail")

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
    Returns a list of all jobs in the system.
    """
    queryset = Job.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = JobSerializer
