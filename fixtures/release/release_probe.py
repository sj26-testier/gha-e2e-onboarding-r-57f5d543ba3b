import json
import os
import subprocess


event = json.load(open(os.environ['GITHUB_EVENT_PATH']))
action = event['action']
release = event['release']
allowed = set(os.environ['ALLOWED_ACTIONS'].split(','))
assert os.environ['GITHUB_EVENT_NAME'] == 'release'
assert action in allowed
assert release['tag_name'] == os.environ['EXPECTED_TAG']
assert release['target_commitish'] == 'main'
assert event['repository']['full_name'] == os.environ['GITHUB_REPOSITORY']
assert os.environ['GITHUB_REF'] == 'refs/tags/' + release['tag_name']
actual = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
assert actual == os.environ['GITHUB_SHA']
expected = os.environ.get('EXPECTED_ACTION')
assert not expected or action == expected
marker = {
    'action': action,
    'actual_sha': actual,
    'draft': release['draft'],
    'event': 'release',
    'prerelease': release['prerelease'],
    'ref': os.environ['GITHUB_REF'],
    'repository': os.environ['GITHUB_REPOSITORY'],
    'sha': os.environ['GITHUB_SHA'],
    'tag': release['tag_name'],
    'workflow': os.environ['WORKFLOW_MARKER'],
}
print('RELEASE_EXECUTED ' + json.dumps(marker, sort_keys=True))
output = os.environ.get('GITHUB_OUTPUT')
if output:
    with open(output, 'a') as handle:
        handle.write('ok=true\n')
