import React from "react";
import './App.css';

import ApiServices from "./ApiServices";
import { JobResultCollectionPanel } from "./JobResultCollectionPanel";
import { SequenceSubmissionForm } from "./SequenceSubmissionForm";


export default class App extends React.Component {
    constructor( props ) {
        super( props );
        this.state = {
            jobs: []
        }
    }

    componentDidMount() {
        this.initializeComponent().catch( ( data ) => {
            console && console.log( "ERROR initializing application!", data )
        } );
    }

    render() {
        return (
            <div className="App">
                <SequenceSubmissionForm className={ "sequence-submission-form"}
                                        onSubmit={ ( sequence ) => this.onSubmit( sequence )}
                />
                <h1>Results</h1>
                <JobResultCollectionPanel jobs={ this.state.jobs }/>
            </div>
      );
    }

    async initializeComponent() {
        const jobs = await ApiServices.fetchJobs();
        this.setState( { jobs } );

        setInterval( async () => {
            const jobs = await ApiServices.refresh();

            this.setState( { jobs } );
        }, 5000 );
    }

    async onSubmit( sequence ) {
        const jobs = await ApiServices.submitJob( sequence );
        this.setState( { jobs } )
    }
}
