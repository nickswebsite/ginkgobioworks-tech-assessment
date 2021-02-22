from celery import shared_task
from celery.utils.log import get_task_logger

from protein_search.models import ProteinSearchJob
from protein_search.search import search


log = get_task_logger(__name__)


@shared_task()
def search_task(sequence, job_id):
    job = ProteinSearchJob.objects.get(pk=job_id)

    log.info(f"beginning job {job.pk}")

    job.job.begin()
    result = search(sequence)

    log.info(f"{job.pk}: search complete.")

    if result:
        job.job.complete()
        job.protein_id = result.protein_id
        job.record_found = result.record_found
        job.record_source = result.record_source
        job.record_description = result.record_description
        job.location_start = result.location.start
        job.location_end = result.location.end
        job.job.message = f"Found: {job.record_found}"
    else:
        job.job.complete(False)
        job.job.message = "no results found"

    job.save()
    job.job.save()

    log.info(f"{job.pk}: job results saved.")
