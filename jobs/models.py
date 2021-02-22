from django.db import models
from django.utils import timezone


class JobState(models.TextChoices):
    PENDING = "PEN", "PENDING"
    IN_PROGRESS = "IPR", "IN_PROGRESS"
    SUCCESSFUL = "YAY", "SUCCESSFUL"
    FAILED = "BOO", "FAILED"


class JobManager(models.Manager):
    def create_job(self, total=10) -> "Job":
        return self.create(
            total=total
        )


class Job(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    ended_on = models.DateTimeField(null=True, blank=True)

    state = models.CharField(max_length=4, choices=JobState.choices, default=JobState.PENDING)
    current = models.IntegerField(default=0)
    total = models.IntegerField(default=10)
    description = models.CharField(max_length=128, default="", blank=True)
    message = models.CharField(max_length=128, default="", blank=True)

    objects = JobManager()

    def begin(self):
        self.state = JobState.IN_PROGRESS

    def complete(self, successful=True):
        if successful:
            self.state = JobState.SUCCESSFUL
        else:
            self.state = JobState.FAILED
        self.ended_on = timezone.now()

    @property
    def pending(self):
        return self.state == JobState.PENDING

    @property
    def successful(self):
        return self.state == JobState.SUCCESSFUL

    @property
    def failed(self):
        return self.state == JobState.FAILED

    @property
    def in_progress(self):
        return self.state == JobState.IN_PROGRESS

    def __str__(self):
        return self.description + f" created on {self.created_on}"
