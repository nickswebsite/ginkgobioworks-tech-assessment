// import { DUMMY_JOBS } from "./DummyData";
//
// const jobs = DUMMY_JOBS
import Cookies from "js-cookie";

const jobs = [];

/* TODO Replace this with a fetch from the server api-root. */
const ApiRoot = {
    proteinSearch: "/protein-search/",
    submitProteinSearch: "/protein-search/start/"
}



async function fetchJobs() {
    const response = await fetch( ApiRoot.proteinSearch );
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
    const csrftoken = Cookies.get("csrftoken");
    const response = await fetch( ApiRoot.submitProteinSearch, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify( { sequence } )
    } );

    if ( response.status === 200 || response.status === 202 ) {
        const newJob = await response.json();

        jobs.push(newJob);
    } else if ( response.status === 400 ) {
        const data = await response.json();

        throw new Error( data.sequence[ 0 ] );
    } else {
        const data = await response.json();

        throw new Error( data.message );
    }

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