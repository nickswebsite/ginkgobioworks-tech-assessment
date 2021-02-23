from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import include, reverse, path
from rest_framework.test import APITestCase, URLPatternsTestCase

import jobs.urls
from protein_search import urls
from protein_search.models import ProteinSearchJob

UserModel = get_user_model()


def create_user(username="user") -> "UserModel":
    return UserModel.objects.create_user(username, "user@example.com", "password")


class ProteinSearchJobModelTests(TestCase):
    def test_create_protein_search_job_saves_the_proper_sequence(self):
        sequence = "catttctatc"

        user = create_user()

        protein_search_job = ProteinSearchJob.objects.create_protein_search_job(sequence, user)

        self.assertEqual(protein_search_job.sequence, sequence.upper())

    def test_create_protein_search_job_assigns_the_proper_owner(self):
        user = UserModel.objects.create_user()

        protein_search_job = ProteinSearchJob.objects.create_protein_search_job("catttctatc", user)

        self.assertEqual(protein_search_job.owner, user)


class ProteinSearchJobApiTests (APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('searches', include(urls)),
        # We need to include jobs.urls to so that the job url can be looked up when serializing search payloads.
        path('jobs', include(jobs.urls)),
    ]

    # CATTTCTATC should be found in NC_007346
    fixture_sequence = "CATTTCTATC"
    fixtures = ["NC_007346.json"]

    def setUp(self) -> None:
        self.user = create_user()
        self.client.force_login(self.user)

    def test_get_jobs_returns_forbidden_if_the_user_is_not_logged_in(self):
        self.client.logout()

        res = self.get_list()

        self.assertEqual(res.status_code, 403)

    def test_get_jobs_returns_an_empty_list_if_there_are_no_jobs(self):
        res = self.get_list()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, [])

    def test_get_jobs_returns_a_users_jobs(self):
        jobs = [
            ProteinSearchJob.objects.create_protein_search_job(sequence, self.user)
               for sequence in ("cat", "tac", "tta")
        ]

        response = self.get_list()

        self.assertEqual(len(response.data), len(jobs))
        for result, job in zip(response.data, jobs):
            self.assertEqual(result["sequence"], job.sequence)

    def test_get_jobs_does_not_return_a_different_users_jobs(self):
        other_user = create_user("other-user")

        for sequence in ("cat", "tac", "tta"):
            ProteinSearchJob.objects.create_protein_search_job(sequence, other_user)

        response = self.get_list()

        self.assertEqual(len(response.data), 0)

    def test_post_sequence_creates_a_new_job(self):
        sequence = "CAT"

        self.post_sequence(sequence)

        self.assertEqual(ProteinSearchJob.objects.count(), 1)

        job: ProteinSearchJob = ProteinSearchJob.objects.all()[0]
        self.assertEqual(job.sequence, sequence)
        self.assertEqual(job.owner, self.user)

    def test_post_sequence_returns_the_proper_response(self):
        response = self.post_sequence(self.fixture_sequence)

        self.assertEqual(response.status_code, 202)

        self.assertEqual(response.data["sequence"], self.fixture_sequence)

        job = ProteinSearchJob.objects.all()[0]
        self.assertEqual(response.data["job"]["state"], job.job.state)
        self.assertEqual(response.data["job"]["current"], job.job.current)
        self.assertEqual(response.data["job"]["total"], job.job.total)

        location = response["Location"]
        self.assertEqual(location, reverse("protein_search-detail", kwargs={"pk": job.pk}))

    def get_list(self):
        url = reverse("protein_search-list")
        return self.client.get(url)

    def post_sequence(self, sequence):
        url = reverse("protein_search-start")
        return self.client.post(url, {"sequence": sequence})
