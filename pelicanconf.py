#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Abhijit Gadgil'
SITENAME = u"Abhijit's Blog"
#SITEURL = u'https://gabhijit.github.io'

PATH = 'content'

TIMEZONE = 'Asia/Calcutta'

DEFAULT_LANG = u'en'



# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('Github', 'https://github.com/gabhijit'),
          ('LinkedIn', 'https://www.linkedin.com/in/amgadgil/'),)

DEFAULT_PAGINATION = 10

DISQUS_SITENAME = 'gabhijit-github-io'

#THEME = "themes/foundation-default-colours"
#THEME = "themes/Just-Read"
THEME = "themes/tuxlite_tbs"

DEFAULT_DATE_FORMAT = '%d/%m/%Y'
REVERSE_ARCHIVE_ORDER = True

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
