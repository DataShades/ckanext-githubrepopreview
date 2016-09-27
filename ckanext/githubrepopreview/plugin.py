import logging
import re

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import requests

from lib import parse

log = logging.getLogger('ckanext.repopreview')

def is_repo(resource_id):
    context = {
        'ignore_auth': True
    }
    try:
        resource = toolkit.get_action('resource_show')(context, {
            'id': resource_id
        })

        return resource.get('github_repository', '') == 'True'
    except:
        return False


def repo_stats(base_url, user=None, password=None):
    def _get_api_url(input_url):
        parsed_info = parse(input_url, False)
        if parsed_info['domain'] in ['github.com', 'www.github.com']:
            base_res_url = "https://api.github.com"
        else:
            # Enterprise domain
            protocol = 'https' if 'https' in input_url else 'http'
            base_res_url = protocol + "://" + parsed_info['domain'] + "/api/v3"

        return base_res_url + "/repos/" + parsed_info['owner'] + "/" + parsed_info['repo']

    def _make_request(input_url):
        if user and password:
            return requests.get(input_url, auth=(user, password))
        else:
            return requests.get(input_url)

    def _count_list(input_url, default_per_page=30):
        raw_request = _make_request(input_url)

        if raw_request.status_code != 200:
            return 0

        if 'link' in raw_request.headers:
            last_page_url = raw_request.headers['link'].split(',')[1].split(';')[0].replace('>', '').replace('<',
                                                                                                             '').strip()
            last_page = int(re.search('.*page=([0-9]*)', last_page_url).group(1))
            last_page_request = _make_request(last_page_url)

            if last_page_request.status_code != 200:
                return default_per_page * (last_page - 1)

            return default_per_page * (last_page - 1) + len(last_page_request.json())
        else:
            return len(raw_request.json())

    r = _make_request(_get_api_url(base_url))

    if r.status_code != 200:
        return None

    base_repo_dict = r.json()
    result = [(u'Name', base_repo_dict['name']), (u'URL', base_repo_dict['html_url']),
              (u'Description', base_repo_dict['description']), (u'Is a Fork', base_repo_dict['fork']),
              (u'Created On', base_repo_dict['created_at']), (u'Last Updated', base_repo_dict['updated_at']),
              (u'Cloned Size', str(round(int(base_repo_dict['size']) / 1024.0, 2)) + "MB"),
              (u'Language', base_repo_dict['language']),
              (u'# of Contributors', _count_list(base_repo_dict['contributors_url'])),
              (u'# of Subscribers', base_repo_dict['subscribers_count']),
              (u'# of Watchers', base_repo_dict['watchers_count']),
              (u'# of Forks', base_repo_dict['forks_count']),
              (u'# of Open Issues', base_repo_dict['open_issues_count']),
              (u'Default Branch', base_repo_dict['default_branch']),
              (u'# of Branches', _count_list(base_repo_dict['branches_url'].split('{')[0])),
              (u'# of Commits Across All Branches', _count_list(base_repo_dict['commits_url'].split('{')[0])),
              (u'# of Tags', _count_list(base_repo_dict['tags_url']))]

    return result


class GitHubRepoPreviewPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IResourceView, inherit=True)
    plugins.implements(plugins.ITemplateHelpers, inherit=False)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')

    def get_helpers(self):
        return {'githubrepopreview_repo_statistics': repo_stats,
                'githubrepopreview_is_repo': is_repo}

    def info(self):
        return {'name': 'githubrepo_view', 'title': 'GitHub Repository Viewer',
                'default_title': 'GitHub Repository Viewer',
                'icon': 'folder-open'}

    def can_view(self, data_dict):
        return is_repo(data_dict['resource']['id'])

    def view_template(self, context, data_dict):
        return 'githubrepo.html'
