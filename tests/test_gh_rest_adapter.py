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
    assert len(response) > gh_default_pagesize
    t1 = TimeStamp.fromFormattedString(response[0]['created_at'], ISO_FORMAT)
    t2 = TimeStamp.fromFormattedString(response[-1]['created_at'], ISO_FORMAT)
    assert t1.asEpochSeconds() > t2.asEpochSeconds()

def test_filter_by_state():
    # curl -i 'https://api.github.com/repos/RallySoftware/churro/pulls?state=open' -u nmusaelian-rally:pass
    repo_name = 'churro'
    owner = config['Organization']
    ref_time_string = '2017-08-23T00:00:00Z'
    state = 'open'    # returns 140+
    #state = 'closed' #returns 3530+
    endpoint = "repos/%s/%s/pulls?state=%s" % (owner, repo_name, state)
    response = gh.get(endpoint)
    print(len(response))
    assert len(response) > gh_default_pagesize
    t1 = TimeStamp.fromFormattedString(response[0]['created_at'], ISO_FORMAT)
    t2 = TimeStamp.fromFormattedString(response[-1]['created_at'], ISO_FORMAT)
    assert t1.asEpochSeconds() > t2.asEpochSeconds()

