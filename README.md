A dirty little script for assigning labels from a tab-separated values sheet.

# github-labels-from-tsv

As a result of Github's new more-useful pull request view and an end-of-year
meeting, [we] decided to start tracking some broad statistics on the code we
write - namely, whether it was [iFixit]-specific, for one or all of our
[Dozuki] customers, or just a general application or infrastructure
improvement.

So, we exported all our org's issues using [github-issues-export], imported
them into Google Docs, and categorized them there (it's much faster than going
through Github's paginated lists).

This script takes in a tab-separated values sheet (as exported from Google
Docs), maps the 'Who For' column into a list of labels, and applies those
labels to the issues.

## Installation and Usage

    [$]> git clone git@github.com:xiongchiamiov/github-labels-from-tsv.git
    [$]> cd github-labels-from-tsv
    [$]> virtualenv --no-site-package --distribute env
    [$]> source env/bin/activate
    [$]> pip install -r requirements.txt
    [$]> ./importer.py 2013\ Github\ Issues\ -\ Sheet\ 1.tsv | tee -a importer.out

Any issues with unknown labels will be skipped after printing an error message:

    [$]> grep 'Unknown label' importer.out
    Unknown label "ii" for https://github.com/iFixit/example-repo/pull/2466
    Unknown label "" for https://github.com/iFixit/example-repo/pull/2461

[we]: https://github.com/orgs/iFixit/members
[iFixit]: http://www.ifixit.com/
[Dozuki]: http://www.dozuki.com/
[github-issues-export]: https://github.com/colmsjo/github-issues-export

