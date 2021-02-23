import ApiServices from "./ApiServices";

function InProgress( props ) {
    return <div>
        In Progress.<br/>
        Started on { props.job.job.created_on }
    </div>
}


function Success( props ) {
    return <table>
        <tr><th>Protein Id</th><td>{ props.job.protein_id }</td></tr>
        <tr><th>Record Found</th><td>{ props.job.record_found }</td></tr>
        <tr><th>Source</th><td>{ props.job.record_source }</td></tr>
        <tr><th>Description</th><td>{ props.job.record_description }</td></tr>
        <tr><th>Location</th><td>{ props.job.location_start } .. { props.job.location_end }</td></tr>
        <tr><th>Job Started On</th><td>{ props.job.job.created_on }</td></tr>
        <tr><th>Job Ended On</th><td>{ props.job.job.ended_on }</td></tr>
    </table>
}


function Failed( props ) {
    return <div>
        Failed: { props.job.job.message }
    </div>
}


function JobSection( props ) {
    if ( props.job.job.state === ApiServices.JOB_STATUS_SUCCESSFUL ) {
        return <Success job={props.job}/>
    } else if ( props.job.job.state === ApiServices.JOB_STATUS_PENDING ) {
        return <InProgress job={ props.job }/>
    } else if ( props.job.job.state === ApiServices.JOB_STATUS_IN_PROGRESS ) {
        return <InProgress job={ props.job }/>
    } else if ( props.job.job.state === ApiServices.JOB_STATUS_FAILED ) {
        return <Failed job={ props.job }/>
    } else {
        /* We should never get here! */
        return <InProgress job={ props.job }/>
    }
}


function jobStateToCssClass( status ) {
    switch ( status ) {
        case ApiServices.JOB_STATUS_SUCCESSFUL:
            return "successful";
        case ApiServices.JOB_STATUS_FAILED:
            return "failed";
        default:
            return "";
    }
}


export function JobResultPanel( props ) {
    const cssClass = jobStateToCssClass( props.job.job.state );

    return <div className={ "job-result " + cssClass }>
        <h1>{ props.job.sequence }</h1>
        <JobSection job={ props.job }/>
    </div>;
}
