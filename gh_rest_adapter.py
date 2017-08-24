import requests

class GitHubResponse:
    def __init__(self):
        self.all_pages  = []
        self.page_count =  0
        self.counter = 0

    def flattenPageResults(self):
        return [item for sublist in self.all_pages for item in sublist]


class GitHubRequest:
    def __init__(self, config):
        self.protocol  = config.get('Protocol', 'https')
        self.server    = config.get('Server',   'api.github.com')
        self.port      = config.get('Port',     443)
        self.user      = config.get('User',     None)
        self.password  = config.get('Password', None)
        self.token     = config.get('Token',    None)
        self.organization = config.get('Organization', None)
        self.pagesize  = config.get('Pagesize', 100)
        self.lookback  = config.get('Lookback', 100)
        self.max_commits = config.get('MaxCommits', 200)
        self.base_url = "{0}://{1}:{2}/".format(self.protocol, self.server, self.port)
        self.connect()

    def connect(self):
        if self.user and self.token:
            self.auth = (self.user, self.token)
        elif self.user and self.password:
            self.auth = (self.user, self.password)
        else:
            return False


    def pageOne(self, url, bucket):
        response = requests.get(url, auth=self.auth)
        bucket.all_pages.append(response.json())
        if response and response.links and response.links.get('last', None):
            bucket.page_count = int(response.links['last']['url'].split('page=')[1])
            bucket.counter = 1
            self.pageNext(response.links['next']['url'], bucket)

    def pageNext(self, url, bucket):
        if bucket.counter < bucket.page_count:
            response = requests.get(url, auth=self.auth)
            bucket.all_pages.append(response.json())
            bucket.counter += 1
            if response.links.get('next', None):
                self.pageNext(response.links['next']['url'], bucket)

    def get(self, endpoint):
        url = self.base_url + endpoint
        bucket = GitHubResponse()
        self.pageOne(url, bucket)
        return bucket.flattenPageResults()