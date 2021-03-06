import logging

from django.urls import reverse
from rest_framework.decorators import action
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import HyperlinkedModelSerializer, Serializer, CharField

from protein_search.models import ProteinSearchJob
from protein_search.validators import DnaValidator
from protein_search.tasks import search_task

log = logging.getLogger(__name__)


def start_search(sequence, owner) -> ProteinSearchJob:
    job = ProteinSearchJob.objects.create_protein_search_job(sequence, owner)

    log.info(f"Delegating protein search {job.pk} for sequence {sequence} started by {owner}")

    result = search_task.apply_async((sequence, job.pk), ignore_result=True)
    result.forget()

    log.info(f"Search job {job.pk} for sequence {sequence} started by {owner} dispatched.")

    return job


class ProteinSearchJobSerializer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name="protein_search-detail")

    class Meta:
        model = ProteinSearchJob
        fields = [
            "url",
            "sequence",
            "protein_id",
            "record_found",
            "record_source",
            "record_description",
            "location_start",
            "location_end",
            "job",
        ]
        depth = 2


class ProteinSearchJobSubmissionSerializer(Serializer):
    sequence = CharField(validators=[DnaValidator()])


class ProteinSearchJobViewSet(ReadOnlyModelViewSet):
    """
    Returns a list of protein search jobs that the user has run.
    """
    queryset = ProteinSearchJob.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProteinSearchJobSerializer

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    @action(methods=["POST"], detail=False, name="start")
    def start(self, request):
        """
        Starts a protein search in the background process. The location of the new job is
        returned in the Location header. The response entity will contain a representation of
        the job in progress.
        """
        serializer = ProteinSearchJobSubmissionSerializer(data=request.data)
        if serializer.is_valid():
            job = start_search(serializer.data.get("sequence"), request.user)
            response_serializer = ProteinSearchJobSerializer(job, context={"request": request})
            return Response(response_serializer.data, status=202, headers={
                "Location": reverse("protein_search-detail", kwargs={"pk": job.pk})
            })
        else:
            return Response(serializer.errors, status=400)

    def get_serializer_class(self):
        if self.action == "start":
            return ProteinSearchJobSubmissionSerializer
        return super().get_serializer_class()
