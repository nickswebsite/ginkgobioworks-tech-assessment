Ginkgo Bioworks Tech Assessment
===============================

Searches a local database for proteins that may be constructed by a
given DNA sequence, (or one similar).


High Level Design
=================

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

* `jobs` - Keeps track of job status. (Note that `jobs` will be extracted out into 
  its own PyPI package.)
* `protein_search` - Provides functionality to search for a protein with a given
  DNA sequence.
* `conf` - Any configurations and settings will be located in a `conf` app.
* `ui` - Serves the end ui.

### Deployment ###

The services will be deployed to a c3 series EC2 instance on AWS. This should prevent
any problems using up CPU credits for long running jobs.

Infrastructure will be managed with Terraform and deployment
will be automated using Ansible scripts.


Development
===========

Install OS Dependencies:

    apt-get install libmysqlclient libmysqlclient-dev

or on Mac

    brew install mysql-client

Install dependencies:

    pip install -r requirements.txt -U

Generate a local settings files, first:

    python manage.py init_dev_environment

Make sure the tests run pass. To run the tests:

    python manage.py test

To run a local development server:

    python manage.py migrate
    python manage.py runserver [PORT_NUMBER]

Note that an in memory celery worker will be spun up when running the development server.

To import a dataset using Entrez visit:

    http://localhost:[PORT_NUMBER]/admin/protein_search/proteindatabaseentry/import-protein-database-entry

Enter a few identifiers separated by whitespace and click `Submit`.

To build a deployable package.

    make image


Contributing
============

To contribute to the project, fork the repository on github, make your changes, and issue a pull request. Please make sure the tests pass before submitting your pull request.


Deployment
==========

To deploy your own instance to AWS, you will need to fill in 

    cd infrastructure
    terraform apply

    cd ../deployment
    ansible-deploy -i infrastructure/inventory deploy.yml


To deploy your own instance to AWS, `terraform` is required (or at least very helpful). You
will need to configure `local.tf` to specify your backend and `local.tfvars` to specify your
credentials.


Roadmap
=======

* Lambda handlers should be implemented to run the background tasks. A little research needs
  to be done to make sure it works with the Django ORM properly.
* Split `jobs` app out into a separate package. This type of boiler plate has been rewritten
  several times across several applications.
