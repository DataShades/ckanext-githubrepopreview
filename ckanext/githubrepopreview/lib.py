import re
from collections import defaultdict

SUPPORTED_ATTRIBUTES = (
    'domain',
    'repo',
    'owner',
    '_user',
    'port',
    'url',
    'platform',
    'protocol',
)


def parse(url, check_domain=True):
    # Values are None by default
    parsed_info = defaultdict(lambda: None)
    parsed_info['port'] = ''

    # Defaults to all attributes
    map(parsed_info.setdefault, SUPPORTED_ATTRIBUTES)

    name = 'github'
    platform = GitHubPlatform()

    for protocol, regex in platform.COMPILED_PATTERNS.items():
        # Match current regex against URL
        match = regex.match(url)

        # Skip if not matched
        if not match:
            # print("[%s] URL: %s dit not match %s" % (name, url, regex.pattern))
            continue

        # Skip if domain is bad
        domain = match.group('domain')
        # print('[%s] DOMAIN = %s' % (url, domain,))
        if check_domain:
            if platform.DOMAINS and not (domain in platform.DOMAINS):
                # print("domain: %s not in %s" % (domain, platform.DOMAINS))
                continue

        # Get matches as dictionary
        matches = match.groupdict()

        # Update info with matches
        parsed_info.update(matches)

        # add in platform defaults
        parsed_info.update(platform.DEFAULTS)

        # Update info with platform info
        parsed_info.update({
            'url': url,
            'platform': name,
            'protocol': protocol,
        })
        return parsed_info

    # Empty if none matched
    return parsed_info


class BasePlatform(object):
    FORMATS = {
        'ssh': r"%(_user)s@%(host)s:%(repo)s.git",
        'http': r"http://%(host)s/%(repo)s.git",
        'https': r"http://%(host)s/%(repo)s.git",
        'git': r"git://%(host)s/%(repo)s.git"
    }

    PATTERNS = {
        'ssh': r"(?P<_user>.+)s@(?P<domain>.+)s:(?P<repo>.+)s.git",
        'http': r"http://(?P<domain>.+)s/(?P<repo>.+)s.git",
        'https': r"http://(?P<domain>.+)s/(?P<repo>.+)s.git",
        'git': r"git://(?P<domain>.+)s/(?P<repo>.+)s.git"
    }

    # None means it matches all domains
    DOMAINS = None
    DEFAULTS = {}

    def __init__(self):
        # Precompile PATTERNS
        self.COMPILED_PATTERNS = dict(
            (proto, re.compile(regex))
            for proto, regex in self.PATTERNS.items()
        )

        # Supported protocols
        self.PROTOCOLS = self.PATTERNS.keys()


class GitHubPlatform(BasePlatform):
    PATTERNS = {
        'https': r'https://(?P<domain>.+)/(?P<owner>.+)/(?P<repo>.+).git',
        'ssh': r'git@(?P<domain>.+):(?P<owner>.+)/(?P<repo>.+).git',
        'git': r'git://(?P<domain>.+)/(?P<owner>.+)/(?P<repo>.+).git',
    }
    FORMATS = {
        'https': r'https://%(domain)s/%(owner)s/%(repo)s.git',
        'ssh': r'git@%(domain)s:%(owner)s/%(repo)s.git',
        'git': r'git://%(domain)s/%(owner)s/%(repo)s.git'
    }
    DOMAINS = ('github.com', 'gist.github.com',)
    DEFAULTS = {
        '_user': 'git'
    }
