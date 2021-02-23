import React from "react";

function isValidDnaCode( char ) {
    return "CATG".indexOf( char ) !== -1;
}


export class SequenceSubmissionForm extends React.Component {
    constructor( props ) {
        super( props );

        this.state = {
            sequence: ""
        }
    }

    render() {
        return <form className="sequence-submission-form">
            <label htmlFor="sequence">Enter Sequence</label>
            <input id="sequence"
                   type={ "text" }
                   name={ "sequence" }
                   value={ this.state.sequence }
                   onChange={ ( event ) => this.onChange( event ) }
            />
            <button onClick={ ( event ) => this.onClick( event ) }>
                Submit
            </button>
        </form>;
    }

    onClick( event ) {
        event.preventDefault();

        if ( this.state.sequence !== "" ) {
            this.props.onSubmit( this.state.sequence );
        }
    }

    onChange( event ) {
        for ( let char of event.target.value ) {
            if ( ! isValidDnaCode( char ) ) {
                return;
            }
        }
        this.setState( { sequence: event.target.value } )
    }
}
