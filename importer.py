#!/usr/bin/env python

# May you recognize your weaknesses and share your strengths.
# May you share freely, never taking more than you give.
# May you find love and love everyone you find.

import csv
import re
import sys

from envoy import run
from github3 import authorize, login

labelMapping = {
   'a': 'r-All',
   'd': 'r-Dozuki',
   'i': 'r-iFixit',
}

# Use a stored OAuth token so we don't have to ask for the user's password
# every time (or save the password on disk!).
token = run('git config --global github-labels-from-tsv.token').std_out.strip()
if not token:
   from getpass import getpass
   user = password = ''

   while not user:
      user = raw_input('Username: ')
   while not password:
      password = getpass('Password: ')

   auth = authorize(user, password,
                    scopes=['repo'],
                    note='github-labels-from-tsv',
                    note_url='https://github.com/xiongchiamiov/github-labels-from-tsv')
   token = auth.token
   # We need to un-unicode token for now.
   # https://github.com/kennethreitz/envoy/issues/34
   run("git config --global github-labels-from-tsv.token '%s'" % str(token))

gh = login(token=token)

# I *really* wanted to do this with repeated nested capture groups, but
# Python's current re module doesn't really support that.  It's probably a good
# thing.
urlExtraction = re.compile(r'https://github.com/([\w-]+)/([\w-]+)/(?:[\w-]+)/([\w-]+)/?')

rows = csv.DictReader(open(sys.argv[1], 'r'), delimiter='\t')
for row in rows:
   try:
      desiredLabel = labelMapping[row['Who For']]
   except KeyError:
      print 'Unknown label "%s" for %s' % (row['Who For'], row['URL'])
      continue
   user, repo, issueNumber = urlExtraction.match(row['URL']).groups()
   issue = gh.issue(user, repo, issueNumber)
   print 'Adding label %s to %s' % (desiredLabel, row['URL'])
   issue.add_labels(desiredLabel)

