copysearch
==========

Search http://www.copyrightevidence.org and more.

.plan
-----

Index content of copyright wiki into elasticsearch. Build a simple API and
search frontend.

More data sources:

* list of [PDF uploads](http://www.copyrightevidence.org/evidence-wiki/index.php/Special:ListFiles) in the wiki
* links from externallinks in the database dump

Pages, with studies:

```
$ find . -name "*html" | grep -v "action" | grep -v "Special:" | grep -v "User:" | grep -E '\([0-9]*\)' | grep -v "title="
```

Access API.

* http://www.copyrightevidence.org/evidence-wiki/api.php

Oh my. http://stackoverflow.com/a/1625291/89391

> I don't think it is possible using the API to get just the text.

----

Done
----

Basic data from wiki. Links to external PDFs.

TODO
----

* download linked PDFs
* extract images from linked PDFs
* harvest some twitter data
* formalize related pages in wiki

API
---

* http://copyrightcentral.arts.gla.ac.uk/wikiData/data

