# ckanext-githubrepopreview

A CKAN plugin for previewing GitHub repository resources.

# Installation

1. Activate you CKAN python environment and install this extension's software::

    $ pyenv/bin/activate

    $ pip install -e  git+https://github.com/DataShades/ckanext-githubrepopreview.git#egg=ckanext-githubrepopreview

2. Enable the extension in your CKAN config file by adding it to ``ckan.plugins``::

    ckan.plugins = githubrepo_view

# Usage

When creating/editing a resource via the UI, check the 'GitHub Repository' checkbox to make this view available. Alternatively, one can update the 'github_repository' extras field of the resource to 'True' via the CKAN API to make the view available.