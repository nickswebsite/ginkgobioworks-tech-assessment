from datetime import timedelta

from django.test import TestCase
from django.urls import include, reverse, path
from django.utils import timezone
from rest_framework.test import APITestCase, URLPatternsTestCase

from jobs import urls
from jobs.models import Job, JobState


class JobModelTests(TestCase):
    def test_create_job_in_pending_state(self):
        job = Job.objects.create_job()

        self.assertEqual(job.state, JobState.PENDING)
        self.assertTrue(job.pending)
        self.assertEqual(job.current, 0)

    def test_create_job_with_the_proper_total(self):
        total = 20

        job = Job.objects.create_job(total)

        self.assertEqual(job.total, total)

    def test_begin_job_sets_the_proper_state(self):
        job = Job.objects.create_job()

        job.begin()

        self.assertEqual(job.state, JobState.IN_PROGRESS)

    def test_create_job_records_the_time_the_job_was_created(self):
        job = Job.objects.create_job()

        self.assertAlmostEqual(job.created_on, timezone.now(), delta=timedelta(seconds=1))


class JobViewsTest(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('', include(urls))
    ]

    def test_get_job_status(self):
        job = Job.objects.create_job()
        job.begin()
        job.current = 2
        job.description = "some-description"
        job.message = "some message"
        job.save()

        url = reverse('job-detail', kwargs={"pk": job.pk})
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["current"], job.current)
        self.assertEqual(res.data["total"], job.total)
        self.assertEqual(res.data["description"], job.description)
        self.assertEqual(res.data["message"], job.message)
        self.assertEqual(res.data["state"], job.state)
        self.assertIsNone(res.data["ended_on"])
