Ginkgo Bioworks Tech Assessment
===============================

High Level Design
-----------------

The system will be implemented using a client/server architecture.

### Client Design ####

The client will be written as a thin ReactJS application with a thin services layer.

Client Services include:

* API Service - responsible for job submission and fetching job status.

React Components:

* `SequenceForm` - Users enter DNA sequences into the Sequence Form to start a new search.
* `JobResultPanel` - Status and results of a job are shown in a `JobResultPanel`.
* `JobResultCollectionPanel` - A container for `JobResultPanels`.

### Server Design ###

The server will be implemented as a Django project delegating background tasks
to a background service using Celery.

The project will contain the following apps:

* `jobs` - Keeps track of job status. (Note that `jobs` will be extracted out into its own PyPI package.)
* `protein_search` - Provides functionality to search for a protein with a given DNA sequence.
* `conf` - Any configurations and settings will be located in a `conf` app.
* `ui` - Serves the end ui.

### Deployment ###

The services will be deployed to a c3 series EC2 instance on AWS. This should prevent
any problems using up CPU credits for long running jobs.

Infrastructure will be managed with Terraform and deployment
will be done using Ansible scripts.
