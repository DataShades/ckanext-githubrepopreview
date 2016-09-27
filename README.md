# ckanext-githubrepopreview

A CKAN plugin for previewing GitHub repository resources.

# Installation

1. Activate you CKAN python environment and install this extension's software::

    $ pyenv/bin/activate

    $ pip install -e  git+https://github.com/DataShades/ckanext-githubrepopreview.git#egg=ckanext-githubrepopreview

2. Enable the extension in your CKAN config file by adding it to ``ckan.plugins``::

    ckan.plugins = githubrepo_view

# Usage

The preview associated with this plugin will become available via the resource manager UI, provided the 'resource_type' for the resource is set to either 'github', 'github_repo', 'github_repository', 'github repo' or 'github repository' (not case sensative). For the view to work, the URL of the resource must GitHub repository URL.