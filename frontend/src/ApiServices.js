// import { DUMMY_JOBS } from "./DummyData";
//
// const jobs = DUMMY_JOBS

const jobs = [];


async function fetchJobs() {
    const response = await fetch( "/protein-search/" );
    const pl = await response.json();

    while ( jobs.length > 0 ) {
        jobs.pop()
    }

    for ( let jobPl of pl ) {
        jobs.push( jobPl );
    }

    return jobs;
}


async function submitJob( sequence ) {
    const newJob = {
        sequence,
        url: "/" + jobs.length + 1,
        "protein_id": "",
        "record_found": "",
        "record_source": "",
        "record_description": "",
        "location_start": -1,
        "location_end": -1,
        "job": {
            "url": "http://localhost:6604/jobs/10/",
            "created_on": "2021-02-21T23:53:37.079210Z",
            "ended_on": null,
            "state": "PEN",
            "current": 0,
            "total": 10,
            "description": "protein search job for admin",
            "message": ""
        },
    }
    jobs.push( newJob );

    return jobs;
}


async function fetchJob( url ) {
    return {
        url,
        sequence: "some-sequence"
    }
}


async function refresh() {
    return await fetchJobs();
}


export default {
    fetchJobs,
    fetchJob,
    submitJob,
    refresh,
    JOB_STATUS_PENDING: "PEN",
    JOB_STATUS_SUCCESSFUL: "YAY",
    JOB_STATUS_FAILED: "BOO",
    JOB_STATUS_IN_PROGRESS: "INP",
}