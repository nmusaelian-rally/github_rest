from gh_rest_adapter import GitHubRequest
from utils.chronuti import TimeStamp, ISO_FORMAT


config = {
        'Protocol'    :  'https',
        'Server'      :  'api.github.com',
        'Port'        :  '443',
        'User'        :  'nmusaelian-rally',
        'Token'       :  'xxxxxx',
        'Organization':  'RallySoftware',
        'Pagesize'    :  '100',
        'Lookback'    :  '15'
}


gh = GitHubRequest(config)
gh_default_pagesize = 30


def test_paging():
    # curl -i 'https://api.github.com/repos/RallySoftware/churro/pulls' -u nmusaelian-rally:pass
    repo_name = 'churro'
    owner = config['Organization']
    endpoint = "repos/%s/%s/pulls" % (owner, repo_name)  # no trailing '/' !!
    response = gh.get(endpoint)
    print (len(response))
    t1 = TimeStamp.fromFormattedString(response[0]['created_at'], ISO_FORMAT)
    t2 = TimeStamp.fromFormattedString(response[-1]['created_at'], ISO_FORMAT)
    assert t1.asEpochSeconds() > t2.asEpochSeconds()


