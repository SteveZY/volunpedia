# -*- coding: iso-8859-1 -*-

import os, uuid

from MoinMoin import wikiutil
from MoinMoin.Page import Page
from MoinMoin.ngowikiutil import NgoWikiUtil 

def execute(pagename, request):
    util = NgoWikiUtil(request)

    if not util.is_super_user():
        return

    util.open_database()

    try:
        util.fixup_database_003()
    finally:
        util.close_database(True)
