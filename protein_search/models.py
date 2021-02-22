from django.contrib.auth import get_user_model
from django.db import models

from jobs.models import Job

UserModel = get_user_model()


class ProteinSearchJobManager(models.Manager):
    def create_protein_search_job(self, sequence, owner) -> "ProteinSearchJob":
        return self.create(
            sequence=sequence.upper(),
            owner=owner,
            job=Job.objects.create_job(10, description=f"protein search job for {owner}"),
        )


class ProteinSearchJob(models.Model):
    objects = ProteinSearchJobManager()

    owner = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="protein_searches")
    sequence = models.TextField(blank=False)
    job = models.OneToOneField(Job, models.CASCADE, related_name="protein_searches")
    record_found = models.CharField(max_length=1024, blank=True, default="")
    record_description = models.TextField(blank=True, default="")
    record_source = models.CharField(max_length=1024, blank=True, default="")
    protein_id = models.CharField(max_length=128, blank=True, default="")
    location_start = models.IntegerField(default=-1)
    location_end = models.IntegerField(default=-1)

    def __str__(self):
        return f"{self.owner.username} - {self.sequence}"


class ProteinDatabaseEntry(models.Model):
    identifier = models.CharField(max_length=1024)
    content = models.TextField()

    def __str__(self):
        return self.identifier
