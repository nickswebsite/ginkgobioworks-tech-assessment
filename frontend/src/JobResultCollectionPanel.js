import { JobResultPanel } from "./JobResultPanel";


export function JobResultCollectionPanel( props ) {
    return <div className="job-results">
        { props.jobs.map( job => <JobResultPanel job={ job } /> ) }
    </div>;
}
